from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response


from .models import Tag, Post, Comment, Like
from .serializers import TagSerializer, PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwner, IsOwnerOrStaff, IsOwnerOrSuperuser


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
    parser_classes = (MultiPartParser,)
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
        "tags": ("exact",),
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

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        if request.user.is_superuser:
            request.data['is_active'] = True
        else:
            request.data['is_active'] = False
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsViewSet(viewsets.ModelViewSet):
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

    def get_serializer_context(self):
        return {"request": self.request}

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
