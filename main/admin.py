from django.contrib import admin
from .models import Profile, Post, Comment, Transaction, AIMentorChat

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "content", "created_at")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount", "created_at")

@admin.register(AIMentorChat)
class AIMentorChatAdmin(admin.ModelAdmin):
    list_display = ("user", "prompt", "response", "created_at")
