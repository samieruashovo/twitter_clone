from rest_framework import viewsets, exceptions
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Comment, Post
from .serializers import (PostForm, PostSerializer, CommentSerializer) #
# from rest_framework.permissions import isAuthenticated
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import generics
from users.models import User
from notifications.models import Notification
from twitter_clone.pagination import CustomPagination
from users.models import User
from itertools import chain
from django.shortcuts import render, redirect

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return list(chain(Post.objects.using('male_user_db').all(), Post.objects.using('female_user_db').all()))
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    def create_post(self, request):
        if request.method =='POST':
            form = PostForm(request.data)
            if form.is_valid():
                post = form.save()
                print(post)
                return Response({'message': 'Tweet created successfully'}, status=201)
            
            return Response({'error': form.error}, status=400)
        

# class PostCommentView(APIView):
#     def get_object
# class ExplorePostViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Post.objects.all()
#     # serializer_class = PostSerializer
#     pagination_class = CustomPagination

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context



