from rest_framework import viewsets, exceptions
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Comment, Post
from .serializers import (PostCommentSerializer, PostForm, PostSerializer)
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
        if request.method == 'POST':
            form = PostForm(request.data)
            if form.is_valid():
                post = form.save()
                print(post)
                return Response({'message': 'Tweet created successfully'}, status=201)

            return Response({'error': form.error}, status=400)


class PostComentView(APIView):
    def get(self, request, pk):
        print(request.data)
        comments = list(chain(Comment.objects.using('male_user_db').filter(
            post_uuid=pk).order_by('-created'), Comment.objects.using('female_user_db').filter(
            post_uuid=pk).order_by('-created')))
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = PostCommentSerializer(
            result_page, many=True, context={'request': request})
        print(serializer.data)
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        data = request.data
        print(data)
        # tweet = self.get_object(pk)
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        new_comment = Comment(body=data.get(
            'body'), username=data.get('username'), gender=data.get('gender'), post_uuid=data.get('post_uuid'))
        new_comment.save()
        # if request.username != tweet.username:
        #     Notification.objects.get_or_create(
        #         notification_type='R',
        #         tweet=tweet,
        #         to_user=tweet.username,
        #         from_user=request.username)
        serializer = PostCommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

# class ExplorePostViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Post.objects.all()
#     # serializer_class = PostSerializer
#     pagination_class = CustomPagination

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context


class PostDetailsView(APIView):
    def get(self, request, uuid):
        print("running22 post")
        print(request.data)
        print(uuid)
        comments = list(chain(Post.objects.using('male_user_db').filter(
            uuid=uuid), Post.objects.using('female_user_db').filter(
            uuid=uuid)))
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = PostSerializer(
            result_page, many=True, context={'request': request})
        print(serializer.data)
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)
