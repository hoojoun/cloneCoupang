from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate
from .models import CustomUser


class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        user = self.cleaned_data.get("username")
        if user.find("@") != -1:
            username = "U_" + user
        else:
            username = "S_" + user
        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.activate:
            raise forms.ValidationError(
                "Your account has disabled.",
                code='inactive',
            )


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'name', 'phone', 'email']
