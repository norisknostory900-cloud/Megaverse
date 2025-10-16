from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from openai import OpenAI
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import (
    User, Profile, Post, Comment, Transaction,
    AIMentorChat, ChatMessage
)
from .serializers import (
    UserSerializer, ProfileSerializer, PostSerializer,
    CommentSerializer, TransactionSerializer,
    AIMentorChatSerializer, ChatMessageSerializer
)

# OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# ---- USER ----
class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


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
            return Response(
                {"error": "Comment content is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = Comment.objects.create(
            post=post, author=request.user, content=content
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


# ---- TRANSACTIONS ----
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        amount = serializer.validated_data.get("amount")

        if amount and amount <= 0:
            raise ValidationError({"amount": "Amount must be positive."})

        serializer.save(sender=sender)


# ---- AI Mentor Chat ----
class AIMentorChatViewSet(viewsets.ModelViewSet):
    queryset = AIMentorChat.objects.all().order_by("-created_at")
    serializer_class = AIMentorChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        prompt = self.request.data.get("prompt", "")
        if not prompt:
            raise ValidationError({"prompt": "Prompt is required."})

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"AI error: {e}"

        serializer.save(user=self.request.user, response=ai_response)


# ---- AI Chat Message ----
class ChatMessageCreateAPIView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_message = serializer.validated_data.get("message", "")
        if not user_message:
            raise ValidationError({"message": "Message is required."})

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"AI error: {e}"

        serializer.save(user=self.request.user, response=ai_response)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        if not post_id:
            raise ValidationError({"post": "Post ID is required"})
        serializer.save(author=self.request.user)
