"""blog_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog_app.views import (
    AuthorCreateAPIView, LoginAPIView, LogoutAPIView,
    PostListCreateAPIView, PostRetrieveDestroyAPIView,
    PostCategoryListCreateAPIView,
    PostCommentCreateAPIView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register', AuthorCreateAPIView.as_view(), name='user_register'),
    path('login', LoginAPIView.as_view(), name='user_login'),
    path('logout', LogoutAPIView.as_view(), name='user_logout'),
    path('categories', PostCategoryListCreateAPIView.as_view(), name='category_list_create'),
    path('posts', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('posts/<int:id>', PostRetrieveDestroyAPIView.as_view(), name='post_retrieve_delete'),
    path('posts/<int:id>/comments', PostCommentCreateAPIView.as_view(), name='post_comment_create')
]
