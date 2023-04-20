from rest_framework import serializers
from .models import Tag, Post, Comment, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time"]
