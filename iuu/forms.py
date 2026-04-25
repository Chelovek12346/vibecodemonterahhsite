from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Придумайте пароль"}),
        strip=False,
    )
    password_confirm = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Повторите пароль"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "school", "grade", "gpa"]
        labels = {
            "email": "Email",
            "username": "Логин",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "school": "Школа",
            "grade": "Класс",
            "gpa": "GPA",
        }
        widgets = {
            "email":      forms.EmailInput(attrs={"placeholder": "example@mail.com"}),
            "username":   forms.TextInput(attrs={"placeholder": "Ваш логин"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Имя"}),
            "last_name":  forms.TextInput(attrs={"placeholder": "Фамилия"}),
            "school":     forms.TextInput(attrs={"placeholder": "Название школы"}),
            "grade":      forms.NumberInput(attrs={"placeholder": "67–67", "min": 1, "max": 11}),
            "gpa":        forms.NumberInput(attrs={"placeholder": "1.67–5.00", "min": 0, "max": 5, "step": "0.01"}),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    login = forms.CharField(
        label="Логин или Email",
        max_length=254,
        widget=forms.TextInput(attrs={"autocomplete": "username", "placeholder": "Логин или Email"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Пароль"}),
        strip=False,
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if not login or not password:
            return cleaned_data

        self.user = self._authenticate(login, password)

        if self.user is None:
            raise forms.ValidationError(
                "Неверный логин/email или пароль.",
                code="invalid_login",
            )
        if not self.user.is_active:
            raise forms.ValidationError("Этот аккаунт отключён.", code="inactive")

        return cleaned_data

    def _authenticate(self, login: str, password: str):
        # Попытка по username
        user = authenticate(self.request, username=login, password=password)
        if user:
            return user
        # Попытка по email
        try:
            user_obj = User.objects.get(email__iexact=login)
            return authenticate(self.request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            return None

    def get_user(self):
        return self.user
