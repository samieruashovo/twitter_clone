from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer
from rest_framework.fields import CurrentUserDefault


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_pic",
            "bio",
            "cover_pic",
            "date_joined",
            "gender"
        ]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    # i_follow = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "profile_pic",
            "bio",
            "cover_pic",
            "date_joined",
            "followers",
            "following",
            "gender",
            "created_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def get_followers(self, obj):
        return obj.followed.count()

    def get_following(self, obj):
        return obj.following.count()

    # def get_i_follow(self,obj):
    #     current_user = self.context.get('request').user
    #     return True if current_user in obj.followed.all() else False

    def validate(self, data):
        if len(data.get("password")) <= 6:
            raise serializers.ValidationError(
                {"error": "Passwords must be larger than 6 letters !"}
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserEditSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    followers = serializers.SerializerMethodField(read_only=True)
    # i_follow = serializers.SerializerMethodField(read_only=True) #check if request.user follow the user
    following = serializers.SerializerMethodField(
        read_only=True
    )  # followers of Profile User

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "profile_pic",
            "bio",
            "cover_pic",
            "email",  # 'i_follow'
            "username",
            "followers",
            "following",
            "bio",
            "gender",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    # def get_i_follow(self,obj):
    #     current_user = self.context.get('request').user
    #     return True if current_user in obj.followed.all() else False

    def get_followers(self, obj):
        return obj.followed.count()

    def get_following(self, obj):
        return obj.following.count()


class UserLessInfoSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "profile_pic", "bio"]
        extra_kwargs = {"password": {"write_only": True}}
