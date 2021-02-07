from django.shortcuts import render
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.authtoken.models import Token


from .models import PostCategory, Post, PostComment
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer,
    PostDetailSerializer, PostCreateSerializer, PostListSerializer,
    PostCategoryListSerializer, PostCategoryCreateSerializer,
    PostCommentCreateSerializer, PostCommentDetailSerializer
)


# Create your views here.
class LoginAPIView(GenericAPIView):
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=serializer.data['email'])
            if not user.check_password(serializer.data['password']):
                raise user_model.DoesNotExist()
            token = Token.objects.get_or_create(user=user)
            response = {
                'token': token[0].key,
                'message': 'Login successful'
            }
            return Response(data=response, status=200)
        except user_model.DoesNotExist:
            response = {
                'message': 'Login failed. Invalid email or password'
            }
            return Response(data=response, status=400)


class LogoutAPIView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        response = {
            'message': 'Logout successful'
        }
        return Response(data=response, status=200)


class AuthorCreateAPIView(GenericAPIView):
    permission_classes = []
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        try:
            user_model.objects.create_user(
                username=serializer.data['email'],
                email=serializer.data['email'],
                password=serializer.data['password'],
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name']
            )
            response = {
                'message': 'New author {} created'.format(serializer.data['email'])
            }
            return Response(data=response, status=201)
        except IntegrityError as e:
            if 'auth_user.username' in e.args[0]:
                raise ValidationError(
                    {'email': ['Author with email: {} already exists.'.format(serializer.data['email'])]}
                )
            else:
                raise e


class PostCategoryListCreateAPIView(ListCreateAPIView):
    # permission_classes = IsAuthenticated,
    queryset = PostCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostCategoryListSerializer
        elif self.request.method == 'POST':
            return PostCategoryCreateSerializer


class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(data=PostDetailSerializer(instance=post).data)


class PostRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    serializer_class = PostDetailSerializer

    def get_object(self):
        try:
            return Post.objects.get(pk=self.kwargs['id'])
        except Post.DoesNotExist:
            raise NotFound(f"Post not found with Id: {self.kwargs['id']}")

        
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author.email == request.user.email:
            post.delete()
            return Response(
                data={'message': 'Post deleted successfully'},
                status=200
            )
        else:
            return Response(
                data={'message': 'You are not authorized to delete this post'},
                status=401
            )


class PostCommentCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostCommentDetailSerializer
        elif self.request.method == 'POST':
            return PostCommentCreateSerializer

    def get_post(self):
        try:
            return Post.objects.get(pk=self.kwargs['id'])
        except Post.DoesNotExist as e:
            raise NotFound(f"Post not found with Id: {self.kwargs['id']}")

    def get_queryset(self):
        post = self.get_post()
        return PostComment.objects.filter(post=post)

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_comment = serializer.save(post=post, commenter=request.user)
        return Response(
            data=PostCommentDetailSerializer(instance=post_comment).data,
            status=201
        )
