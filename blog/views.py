from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Tag, Post, Comment, Like
from .serializers import TagSerializer, PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwner, IsOwnerOrStaff, IsOwnerOrSuperuser, IsSuperuser


# TODO : Explain all blog features about likes and comments
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_fields = {
        "name": ("exact", "icontains"),
    }

    def get_permissions(self):
        """
        Determines permission classes based on the action.

        For actions "list" and "retrieve", it allows any user. For other actions,
        only admin users are allowed.

        Returns:
        - list: A list of instantiated permission classes.
        """
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
        """
        Retrieves a queryset of Post objects based on user permissions.

        If the user is a superuser, it returns all Post objects. Otherwise,
        it returns only the active Post objects.

        Returns:
        - QuerySet: A queryset of Post objects.
        """
        user = self.request.user
        return Post.objects.all() if user.is_superuser else Post.objects.filter(is_active=True)

    def get_permissions(self):
        """
        Determines permission classes based on the action being performed.

        - For actions "list" and "retrieve": any user is allowed.
        - For actions "update", "partial_update", and "destroy": only the owner or a superuser is allowed.
        - For the action "approve_post": only a superuser is allowed.
        - For all other actions: only admin users are allowed.

        Returns:
        - list: A list of instantiated permission classes.
        """
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsOwnerOrSuperuser]
        elif self.action == "approve_post":
            permission_classes = [IsSuperuser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to handle post creation.

        After saving the post, the method checks if the user is a superuser. If so,
        the post's `is_active` attribute is set to True; otherwise, it's set to False.

        Args:
        - request (Request): The HTTP request object containing post data.
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.

        Returns:
        - Response: Serialized post data with a status of HTTP 201 CREATED.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        if request.user.is_superuser:
            post.is_active = True
        else:
            post.is_active = False
        post.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=["post"], detail=True)
    def approve_post(self, request, pk=None):
        """
        Approves a post by setting `is_active` to True.

        Args:
        - request (Request): The HTTP request object.
        - pk (int, optional): The primary key of the post.

        Returns:
        - Response: Message indicating approval with HTTP 202 ACCEPTED status.
        """
        post = self.get_object()
        post.is_active = True
        post.save()
        return Response({"message": "Post approved"}, status=status.HTTP_202_ACCEPTED)


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
        "is_active": ("exact",),
    }

    def get_serializer_context(self):
        """
        Provides the current request to the serializer context.

        Returns:
        - dict: Dictionary containing the current request object.
        """
        return {"request": self.request}

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.all() if user.is_superuser else Comment.objects.filter(is_active=True)

    def get_permissions(self):
        """
        Determines permission classes based on the action being performed.

        - "update" or "partial_update" requires the user to be the owner.
        - "destroy" allows either the owner or staff.
        - All other actions allow any user.

        Returns:
        - list: Instantiated permission classes based on the action.
        """
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
        """
        Determines permission classes based on the action.

        - "list", "retrieve", or "create" actions allow any user.
        - All other actions require the user to be the owner or a staff member.

        Returns:
        - list: Instantiated permission classes for the current action.
        """
        if self.action in ["list", "retrieve", "create"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwnerOrStaff]
        return [permission() for permission in permission_classes]
