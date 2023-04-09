from django.contrib import admin

from .models import Tag, GalleryImage, Post, Comment, Like


admin.site.register(Tag)
admin.site.register(GalleryImage)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
