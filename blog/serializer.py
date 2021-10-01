from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'comment_text']


class PostsSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:

        model = Posts
        fields = ['id', 'user', 'title', 'text', 'comments']


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ['id', 'user_id', 'following_user_id', 'created']


class FollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ['id', 'user_id', 'created']


class UserSerializer(serializers.ModelSerializer):

    following = FollowingSerializer(many=True, read_only=True)
    followers = FollowersSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'following', 'followers']
        extra_kwargs = {'password': {'write_only': True}}

    def get_following(self, obj):
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data