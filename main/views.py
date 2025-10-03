from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Transaction, AIMentorChat
from .serializers import (
    UserSerializer, ProfileSerializer, PostSerializer,
    CommentSerializer, TransactionSerializer, AIMentorChatSerializer
)


# ---- USER ----
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# ---- PROFILE ----
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---- POSTS ----
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def comment(self, request, pk=None):
        """Postga komment qo‘shish"""
        post = self.get_object()
        content = request.data.get("content")
        if not content:
            return Response({"error": "Comment content is required"}, status=400)
        comment = Comment.objects.create(post=post, author=request.user, content=content)
        return Response(CommentSerializer(comment).data)


# ---- TRANSACTIONS ----
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


# ---- AI Mentor Chat ----
class AIMentorChatViewSet(viewsets.ModelViewSet):
    queryset = AIMentorChat.objects.all().order_by("-created_at")
    serializer_class = AIMentorChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        prompt = self.request.data.get("prompt", "")
        # Mock javob (hozircha faqat test uchun)
        fake_response = f"AI javobi: {prompt[::-1]}"
        serializer.save(user=self.request.user, response=fake_response)
