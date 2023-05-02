from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Tag, Post, Comment, Like, GalleryImage


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time", "user"]


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time", "user"]

    def validate(self, data):
        user = self.context.get("request").user
        if not user.is_authenticated:
            if not data.get("name"):
                raise ValidationError({"name": "This field may not be blank."})
            if not data.get("email"):
                raise ValidationError({"email": "This field may not be blank."})
        return data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time"]
