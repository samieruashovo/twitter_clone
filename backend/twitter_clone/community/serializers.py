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
            'id','body',
            
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
        fields = ["title", "username", "body", "liked", "image", "gender"]


class PostSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    # iliked = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)
    myparent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_like_count(self, obj):
        return 0
        #return obj.liked.count()

    def get_username(self, obj):
        return "obj.username"

    def get_myparent(self, obj):
        serializers = PostSerializer(context={"request": self.context.get("request")}, many=True)
        return serializers.data
    def get_gender(self, obj):
        return "obj.gender1"
    
    def get_iliked(self, obj):
        return (
            True if self.context.get("request").username in obj.liked.all() else False
        )
    def get_comment_count(self, obj):
        return "S"