from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ["email", "username"] #pyright:ignore
        error_class = "error" #pyright:ignore


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["email", "username"]
        error_class = "error"