from rest_framework import serializers
from .models import Comment, Post
from rest_framework.response import Response
from django import forms


class PostCommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True, many=False)
    # iliked = serializers.SerializerMethodField(read_only=True)
    # is_parent = serializers.SerializerMethodField(read_only=True)
    # children = serializers.SerializerMethodField(read_only=True)
    # parentId= serializers.SerializerMethodField(read_only=True)
    # like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'body',

            'created',
        ]


class UserPostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_like_count(self, obj):
        return 0
        # return obj.liked.count()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []


class PostSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    # iliked = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    # gender = serializers.SerializerMethodField(max_length=200, allow_blank=True)
    myparent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('uuid', 'title', 'username', 'body', 'liked', 'image',
                  'gender', 'like_count', 'comment_count', 'myparent')
        read_only_fields = ('uuid', 'like_count', 'comment_count', 'myparent')
        # exclude = ('uuid',)

    def get_like_count(self, obj):
        return 0
        # return obj.liked.count()

    def get_username(self, obj):
        return obj.username

    def get_myparent(self, obj):
        serializers = PostSerializer(
            context={"request": self.context.get("request")}, many=True)
        return serializers.data

    def get_gender(self, obj):
        return obj.gender

    def get_iliked(self, obj):
        return (
            True if self.context.get(
                "request").username in obj.liked.all() else False
        )

    def get_comment_count(self, obj):
        return "S"
