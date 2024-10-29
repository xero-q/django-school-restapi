from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest

class CustomBackend(BaseBackend):
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        User = get_user_model()
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        User = get_user_model()

        try:
            return User.objects.get(pk=user_id)           
        except User.DoesNotExist:
            return None