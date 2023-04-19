from django.contrib import admin

from .models import Tag, GalleryImage, Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "is_active", "created_time", "updated_time")
    list_filter = ("user__username", "is_active")
    search_fields = ("title", "user__username")
    list_per_page = 50


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_per_page = 100


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment_text", "post", "user", "is_active", "created_time", "updated_time")
    list_filter = ("user__username", "is_active")
    search_fields = ("comment_text", "user__username")
    list_per_page = 100


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "liked", "user", "is_active", "content_type", "content", "created_time", "updated_time")
    list_filter = ("user__username", "liked", "is_active")
    search_fields = ("user__username",)
    list_per_page = 100


admin.site.register(GalleryImage)
