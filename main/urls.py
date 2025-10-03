from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet, PostViewSet,
    TransactionViewSet, AIMentorChatViewSet
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)
router.register(r"transactions", TransactionViewSet)
router.register(r"ai-chat", AIMentorChatViewSet)

urlpatterns = router.urls
