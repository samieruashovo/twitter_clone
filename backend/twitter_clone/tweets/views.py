from django.db import connections
from django_filters.rest_framework import DjangoFilterBackend
from users.serializers import UserLessInfoSerializer
from rest_framework import filters
from rest_framework import viewsets, exceptions
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Tweet, Comment
from .serializers import (TweetForm, TweetSerializer, CommentSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import generics
from users.models import User
from notifications.models import Notification
from twitter_clone.pagination import CustomPagination
from users.models import User
from itertools import chain
from django.shortcuts import render, redirect
import os
from django.http import FileResponse
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import mimetypes


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        return list(chain(Tweet.objects.using('male_user_db').all(), Tweet.objects.using('female_user_db').all()))

        # return Tweet.objects.using('female_user_db').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        print('context: ')
        return context

    def create_tweet(self, request):
        if request.method == 'POST':

            form = TweetForm(request.data)
            print('x')
        #    print(form)
            if form.is_valid():
                print('y')
                tweet = form.save(commit=False)
                print(tweet)
                # Set username based on the authenticated user
                tweet.username = request.user.username
                tweet.save()
                # Redirect to a success page or another view
                return Response({'message': 'Tweet created successfully'}, status=201)
        return Response({'errors': form.errors}, status=400)

    # def perform_create(self, serializer):
    #     print("view_set: ")
    #     print(self.request.user.gender)
    #     print(serializer)
    #     try:
    #        serializer.save(username=self.request.user.username)

    #     except Exception as e:
    #         print("Error creating Tweet instance:", e)
# @api_view(['POST'])

        # if self.request.user.gender =='male':
        #     print("gender platform_create male")
        #     serializer.save(username=self.request.user.username, using='male_user_db')
        # elif self.request.user.gender =='female':
        #     print("gender platform_create female")
        #     serializer.save(username=self.request.user.username, using='male_user_db')
        # else:
        #     print("gender platform_create default")
        #     serializer.save(username=self.request.user.username)


# class FemaleTweetViewSet(viewsets.ModelViewSet):
#     queryset = FemaleTweet.objects.all()
#     serializer_class = FemaleTweetSerializer
#     pagination_class = CustomPagination
#     permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

#     def get_queryset(self):
#         return FemaleTweet.objects.only_public_or_author(self.request.user)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


class ExploreTweetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def ReTweetView(request):
    data = request.data
    tweetId = data["tweetId"]
    # tweet = get_object_or_404(Tweet,id=tweetId)
    try:
        tweet = Tweet.objects.using('default').get(id=tweetId)
    except:
        raise exceptions.APIException("Not Found ! ")
    if tweet.username == request.username:
        raise exceptions.APIException("Can't Retweet your own post")
    # try:
    parent_tweet = Tweet.objects.using('default').filter(
        parent=tweet, username=request.username)
    if parent_tweet.exists():
        raise exceptions.APIException("Already retweeted !")
    else:
        re_tweet = Tweet.objects.using('default').create(
            username=request.username,
            parent=tweet
        )
        Notification.objects.using('default').get_or_create(
            notification_type='RT',
            tweet=tweet,
            to_user=tweet.username,
            from_user=request.user)
        serializer = TweetSerializer(re_tweet, context={"request": request})
        return Response(serializer.data, status=HTTP_201_CREATED)


class ComentView(APIView):
    def get(self, request, pk):
        print("running2")
        print(request.data)
        print(pk)
        comments = list(chain(Comment.objects.using('male_user_db').filter(
            tweet_uuid=pk).order_by('-created'), Comment.objects.using('female_user_db').filter(
            tweet_uuid=pk).order_by('-created')))
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(
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
            'body'), username=data.get('username'), gender=data.get('gender'), tweet_uuid=data.get('tweet_uuid'))
        new_comment.save()
        # if request.username != tweet.username:
        #     Notification.objects.get_or_create(
        #         notification_type='R',
        #         tweet=tweet,
        #         to_user=tweet.username,
        #         from_user=request.username)
        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)


class TweetDetailsView(APIView):
    def get(self, request, uuid):
        print("running22")
        print(request.data)
        print(uuid)
        comments = list(chain(Tweet.objects.using('male_user_db').filter(
            uuid=uuid).order_by('-created'), Tweet.objects.using('female_user_db').filter(
            uuid=uuid).order_by('-created')))
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = TweetSerializer(
            result_page, many=True, context={'request': request})
        print(serializer.data)
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)


# class SinglePostCommentViewSetc(viewsets.ViewSet):
#     @api_view(['GET'])
#     def list(self, request):
#         print("running 3xx")
#         if request.method == 'GET':
#             # tweets = Tweet.objects.using('male_user_db').all()
#             serializer = CommentSerializer(
#                  many=True, context={'request': request})
#             return Response(serializer.data)
# single_post_comment_view = SinglePostCommentViewSetc.as_view({'get': 'list'})

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def ComentReplyView(request, pk):
    data = request.data
    if request.method == 'POST':
        tweet = Tweet.objects.get(id=pk)
        parentComId = data.get('comId')
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        parent = Comment.objects.get(id=parentComId)
        new_comment = Comment(parent=parent, body=data.get(
            'body'), username=request.username, post=tweet)
        new_comment.save()
        if request.username != parent.username:
            Notification.objects.get_or_create(
                notification_type='R',
                comment=parent,
                to_user=parent.username,
                tweet=tweet,
                from_user=request.username)

        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data, status=HTTP_201_CREATED)

# {
# "uuid": "fff4a097dba1472c9d0ed81e1d8a3b10",
# "username": "shovo"
# }


@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def like_unlike_tweet(request):
    if request.method == "POST":
        print("xxxx")
        # print(request.data)
        pk = request.data.get("uuid")
        usrname = request.data.get('username')
        # print(pk + usrname)
        # tweet = list(chain(Tweet.objects.using('male_user_db').all(),
        #              Tweet.objects.using('female_user_db').all()))
        # print(tweet)
        # # Replace 'db1' with the actual database alias.
        # tweet_db1 = Tweet.objects.using('male_user_db').get(Tweet.objects.using("female_user_db"), uuid=pk)

        # # Connect to the second database
        # # Replace 'db2' with the actual database alias.
        # tweet_db2 = Tweet.objects.using('female_user_db').get(Tweet, uuid=pk)
        # print(tweet_db1)
        # print(tweet_db2)

        # print(get_object_or_404(Tweet.objects.using(
        #     "female_user_db"), uuid=pk) + "xxxx")
        try:
            tweet = get_object_or_404(Tweet.objects.using(
                "female_user_db"), uuid=pk)
        except:
            tweet = get_object_or_404(Tweet.objects.using(
                "male_user_db"), uuid=pk)
        print(tweet)

        # print(tweet + "skjd")

        # print(tweet.liked.split(','))

        if usrname not in tweet.liked.split(','):
            tweet.liked += f',{usrname}'
            print(tweet.liked)
            tweet.save()
        else:
            liked_list = tweet.liked.split(',')
            liked_list.remove(usrname)
            tweet.liked = ','.join(liked_list)
            print(tweet.liked)
            tweet.save()

        # if request.user in tweet.liked.all():
        #     liked = False
        #     tweet.liked.remove(request.username)
        # else:
        #     liked = True
        #     tweet.liked.add(request.username)
        #     if request.username != tweet.username:
        #         Notification.objects.get_or_create(
        #             notification_type='L',
        #             tweet=tweet,
        #             to_user=tweet.username,
        #             from_user=request.username)
        return Response({
            'liked': tweet.liked,
            'count': tweet.like_count
        })
# def add_like(self, username):
#         if username not in self.liked.split(','):
#             self.liked += f',{username}'
#             self.save()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like_unlike_comment(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        comment = get_object_or_404(Comment, id=pk)
        if request.user in comment.liked.all():
            liked = False
            comment.liked.remove(request.user)
        else:
            liked = True
            comment.liked.add(request.user)
            if request.user != comment.author:
                Notification.objects.get_or_create(
                    notification_type='LR',
                    comment=comment,
                    to_user=comment.author,
                    from_user=request.user)
        return Response({
            'liked': liked,
            'count': comment.like_comment
        })


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def bookmark_tweet(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user in tweet.bookmark.all():
            bookmarked = False
            tweet.bookmark.remove(request.user)
        else:
            bookmarked = True
            tweet.bookmark.add(request.user)
        return Response({
            'bookmarked': bookmarked,
        })


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def UserTweetList(request, username):
    print("running 3")
    user = User.objects.get(username=username)
    if request.method == 'GET':
        tweets = Tweet.objects.filter(username=username).filter(
            is_private=False).order_by('-created')
        if user == request.user:
            owner_private = Tweet.objects.filter(
                username=request.username).filter(is_private=True)
            tweets = tweets | owner_private
        serializer = TweetSerializer(
            tweets, many=True, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def bookmarkList(request):
    print("running 3")

    bookmark_tweet = request.user.bookmark.all().order_by('-id')
    serializer = TweetSerializer(
        bookmark_tweet, many=True, context={'request': request})
    return Response(serializer.data)


class SearchList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLessInfoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('username', 'first_name', 'last_name')


def serve_image(request, image_filename):
    image_path = os.path.join(settings.MEDIA_ROOT, image_filename)

    try:
        # Open the file in binary read mode and keep it open until it's served.
        image_file = open(image_path, 'rb')
        response = FileResponse(image_file)
        # Determine and set the content type based on the file extension.
        content_type, encoding = mimetypes.guess_type(image_path)
        response['Content-Type'] = content_type
        return response
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error serving the image: {str(e)}", status=500)
