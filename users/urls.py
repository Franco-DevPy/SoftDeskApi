from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path
from .views import RegisterView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]


urlpatterns += router.urls
