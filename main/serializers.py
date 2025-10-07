from .models import Profile, Post, Comment, Transaction, AIMentorChat, ChatMessage
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar_url', 'oauth_provider']



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "avatar", "balance"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "author", "content", "created_at", "comments"]

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]


class TransactionSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ["id", "sender", "receiver", "amount", "created_at"]


class AIMentorChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMentorChat
        fields = ["id", "user", "prompt", "response", "created_at"]
        read_only_fields = ["response", "user"]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'response', 'timestamp']
        read_only_fields = ['response', 'timestamp']