from django.urls import path, include
from rest_framework import routers

from .views import TagsViewSet, PostsViewSet, CommentsViewSet, LikesViewSet, ContentTypeListView


app_name = "blog"

router = routers.DefaultRouter()
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"posts", PostsViewSet, basename="posts")
router.register(r"comments", CommentsViewSet, basename="comments")
router.register(r"likes", LikesViewSet, basename="likes")


urlpatterns = [
    path("", include(router.urls)),
    path("contenttypes/", ContentTypeListView.as_view(), name="contenttype-list"),
]
