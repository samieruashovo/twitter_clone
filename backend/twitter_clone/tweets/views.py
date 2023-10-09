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
               tweet.username = request.user.username  # Set username based on the authenticated user
               tweet.save()
               return Response({'message': 'Tweet created successfully'}, status=201) # Redirect to a success page or another view
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
    parent_tweet = Tweet.objects.using('default').filter(parent=tweet, username=request.username)
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
        serializer =  TweetSerializer(re_tweet,context={"request":request})
        return Response(serializer.data,status=HTTP_201_CREATED)


    



class ComentView(APIView):
    # permission_classes= [IsAuthenticated]

    def get_object(self,pk):
        tweet = Tweet.objects.get(id=pk)
        return tweet

    def get(self, request,pk):
        tweet = self.get_object(pk)
        comments = Comment.objects.filter(
            post=tweet, parent=None).order_by('-created')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(comments,request)
        serializer = CommentSerializer(
            result_page, many=True, context={'request': request})
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    def post(self,request,pk):
        data = request.data
        tweet = self.get_object(pk)
        if len(data.get('body')) < 1:
            raise exceptions.APIException('Cannot be blank')
        new_comment = Comment(body=data.get(
            'body'), username=request.username, post=tweet)
        new_comment.save()
        if request.username != tweet.username:
            Notification.objects.get_or_create(
                notification_type='R',
                tweet=tweet,
                to_user=tweet.username,
                from_user=request.username)
        serializer = CommentSerializer(
            new_comment, context={'request': request})
        return Response(serializer.data,status=HTTP_201_CREATED)


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
        return Response(serializer.data,status=HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like_unlike_tweet(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        tweet = get_object_or_404(Tweet, id=pk)

        if request.user in tweet.liked.all():
            liked = False
            tweet.liked.remove(request.username)
        else:
            liked = True
            tweet.liked.add(request.username)
            if request.username != tweet.username:
              Notification.objects.get_or_create(
                    notification_type='L',
                    tweet=tweet,
                    to_user=tweet.username,
                    from_user=request.username)
        return Response({
            'liked': liked,
            'count': tweet.like_count
        })



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
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def bookmarkList(request):
    bookmark_tweet = request.user.bookmark.all().order_by('-id')
    serializer = TweetSerializer(
        bookmark_tweet, many=True, context={'request': request})
    return Response(serializer.data)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from users.serializers import UserLessInfoSerializer

class SearchList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLessInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ('username','first_name','last_name')