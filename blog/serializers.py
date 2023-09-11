from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Tag, Post, Comment, Like, GalleryImage


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ("file_name",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, required=False, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_username = serializers.ReadOnlyField(source="user.username")
    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time", "user"]

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)

        for image_data in images_data:
            GalleryImage.objects.create(post=post, **image_data)

        return post


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["is_active", "created_time", "updated_time", "user"]

    def validate(self, data):
        """
        Validates the provided data for user authentication.

        Parameters:
        - data (dict): A dictionary containing user data, expected to have "name" and "email" keys.

        Returns:
        - dict: The validated data.

        """
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


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"
