from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from .forms import UserLoginForm
from .views import UserRegisterView, PasswordsChangeView
from . import views


app_name = "users"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=UserLoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', views.Profile_Update, name="profile_update"),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_updated', views.password_updated, name='password_updated'),
    path("password_reset/", auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<slug:uidb64>/<slug:token>/", 
        auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("users:password_reset_complete")), 
        name="password_reset_confirm"
    ),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]

