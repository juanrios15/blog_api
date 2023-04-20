from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Tag, Post, Comment, Like
from .serializers import TagSerializer, PostSerializer, CommentSerializer, LikeSerializer


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return obj.user == request.user


class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_fields = {
        "name": ("exact", "icontains"),
    }

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filterset_fields = {
        "title": ("icontains",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
        "user": ("exact",),
        "user__username": ("icontains",),
        "tags": ("exact", "in"),
        "is_active": ("exact",),
    }

    def get_queryset(self):
        user = self.request.user
        return Post.objects.all() if user.is_superuser else Post.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif self.action == "update" or self.action == "partial_update" or self.action == "destroy":
            permission_classes = [IsOwnerOrSuperuser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    filterset_fields = {
        "comment_text": ("icontains",),
        "post": ("exact", "in"),
        "user": ("exact",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
        "previous_comment": ("exact",),
    }

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.all() if user.is_superuser else Comment.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == "update" or self.action == "partial_update":
            permission_classes = [IsOwner]
        elif self.action == "destroy":
            permission_classes = [IsOwnerOrStaff]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LikesViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    filterset_fields = {
        "user": ("exact",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
    }

    def get_queryset(self):
        user = self.request.user
        return Like.objects.all() if user.is_superuser else Like.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve" or self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrStaff]
        return [permission() for permission in permission_classes]
