from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router obyekti — viewsetlar uchun
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'profiles', views.ProfileViewSet, basename='profile')
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'aimentor-chats', views.AIMentorChatViewSet, basename='ai-mentor-chat')

urlpatterns = [
    # ---- REST router ----
    path('', include(router.urls)),

    # ---- Authenticated user (GET/PUT) ----
    path('user/me/', views.UserRetrieveUpdateAPIView.as_view(), name='user-me'),

    # ---- AI Chat message creation ----
    path('chat-messages/create/', views.ChatMessageCreateAPIView.as_view(), name='chat-message-create'),
]
