from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import PostCategory, Post, PostComment


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=250, required=True)
    password = serializers.CharField(max_length=25, required=True, validators=[validate_password])


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=25, required=True)
    last_name = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField(max_length=250, required=True)
    password = serializers.CharField(max_length=25, required=True, validators=[validate_password])


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class PostCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ('name', )


class PostCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content')


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('content', )


class PostCommentDetailSerializer(serializers.ModelSerializer):
    commenter = UserDetailSerializer()
    class Meta:
        model = PostComment
        exclude = ('post', )


class PostListSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    category = serializers.SerializerMethodField('get_category_name')
    class Meta:
        model = Post
        fields = '__all__'

    def get_category_name(self, instance):
        return instance.category.name


class PostDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category_name')
    author = UserDetailSerializer()
    comments = PostCommentDetailSerializer(many=True)
    class Meta:
        model = Post
        fields = '__all__'

    def get_category_name(self, instance):
        return instance.category.name