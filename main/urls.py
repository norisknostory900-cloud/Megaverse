from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'aimentor-chats', views.AIMentorChatViewSet)
router.register(r'comments', views.CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('user/me/', views.UserRetrieveUpdateAPIView.as_view(), name='user-me'),
    path('chat-messages/create/', views.ChatMessageCreateAPIView.as_view(), name='chat-message-create'),
]
