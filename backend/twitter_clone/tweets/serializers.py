from rest_framework import serializers
from .models import Comment, Tweet
from users.serializers import UserSerializer
from users.models import User
from rest_framework.response import Response
from users.serializers import UserLessInfoSerializer
from django import forms


class CommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True, many=False)
    # iliked = serializers.SerializerMethodField(read_only=True)
    # is_parent = serializers.SerializerMethodField(read_only=True)
    # children = serializers.SerializerMethodField(read_only=True)
    # parentId= serializers.SerializerMethodField(read_only=True)
    # like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'body', 'created', 'tweet_uuid', 'username'
        ]
    # def get_iliked(self,obj):
    #     return True if self.context.get('request').user in obj.liked.all() else False

    # def get_is_parent(self,obj):
    #     return obj.is_parent

    # def get_parentId(self,obj):
    #     if obj.parent:
    #         return obj.parent.id
    #     return None

    # def get_children(self,obj):
    #     serializer = CommentSerializer(obj.children, many=True,
    #     context={'request':self.context.get('request')})
    #     return serializer.data

    # def get_like_count(self,obj):
    #     return obj.liked.count()


class UserTweetSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True, many=False)
    like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.liked.count()


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['title', 'username', 'body', 'image',
                  'is_private', 'gender', 'is_parent', 'liked']


class TweetSerializer(serializers.ModelSerializer):
   # author = UserSerializer(read_only=True, many=False)
    # username = serializers.SerializerMethodField(read_only=True)
    iliked = serializers.SerializerMethodField(read_only=True)
    # i_bookmarked = serializers.SerializerMethodField(read_only=True)
    # like_count = serializers.SerializerMethodField(read_only=True)
    # myparent = serializers.SerializerMethodField(read_only=True)
    # comment_count = serializers.SerializerMethodField(read_only=True)
    # gender = serializers.SerializerMethodField(read_only=True)

    class Meta:
        # using = 'default'
        model = Tweet
        fields = '__all__'

    def get_myparent(self, obj):

        # all_tweets = Tweet.objects.all()
        # female_tweets = Tweet.objects.using('female_user_db').all()
        # male_tweets = Tweet.objects.using('male_user_db').all()
        # combined_tweets = male_tweets.union(female_tweets)
        # combined_tweets = list(male_tweets) + list(female_tweets)
        serializer = TweetSerializer(
            context={'request': self.context.get('request')}, many=True)
        print("test01")
        # print(serializer.data)
        return serializer.data

    def get_username(self, obj):
        # print(obj)
        # if obj.db == 'male_user_db':
        #     return obj.username
        # elif obj.db == 'female_user_db':
        #     return obj.username
        # else:
        #     return 'shovo'
        return obj.username

    def get_gender(self, obj):
        return obj.gender
    # def iliked(self, username):
    #     if username in self.liked.split(','):
    #         return True
    #     return False

    def get_iliked(self, obj):
        print("asdf")
        liked_list = [username.strip()
                      for username in obj.liked.split(',') if username.strip()]
        request = self.context.get('request')
        print(request.user)
        print(liked_list)

        if str(request.user).lower() not in [username.lower() for username in liked_list]:
            print("false")
            return False
        return True
        # print('user liked :', obj.liked.all())
        # print('me is ',self.context.get('request').user)
        # return True if self.context.get('request').user in obj.liked.all() else False

    def get_i_bookmarked(self, obj):
        return False
        # return True if self.context.get('request').user in obj.bookmark.all() else False

    def get_like_count(self, obj):
        return obj.liked.count()

    def get_comment_count(self, obj):
        return obj.parent_tweet.count()


# class FemaleTweetSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True, many=False)
#     iliked = serializers.SerializerMethodField(read_only=True)
#     i_bookmarked = serializers.SerializerMethodField(read_only=True)
#     like_count = serializers.SerializerMethodField(read_only=True)
#     myparent = serializers.SerializerMethodField(read_only=True)
#     comment_count = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = FemaleTweet
#         fields = '__all__'

#     def get_myparent(self,obj):
#         serializer = TweetSerializer(obj.parent,
#         context={'request':self.context.get('request')})
#         return serializer.data

#     def get_iliked(self,obj):
#         print('user liked :', obj.liked.all())
#         print('me is ',self.context.get('request').user)
#         return True if self.context.get('request').user in obj.liked.all() else False

#     def get_i_bookmarked(self,obj):
#         return True if self.context.get('request').user in obj.bookmark.all() else False

#     def get_like_count(self,obj):
#         return obj.liked.count()
#     def get_comment_count(self,obj):
#         return obj.parent_tweet.count()


class AnonTweetSerializer(serializers.ModelSerializer):
    # author = UserLessInfoSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'title', 'username']


class LessCommentSerializer(serializers.ModelSerializer):
    tweet_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'tweet_id']

    def get_tweet_id(self, obj):
        return obj.post.id
