from django.urls import path

from users.apps import UsersConfig
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [] + router.urls