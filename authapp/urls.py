from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView

from authapp import views
from authapp.apps import AuthappConfig

app_name = AuthappConfig.name

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile_edit/<int:pk>", views.ProfileEditView.as_view(), name="profile_edit"),
    path("profile_info/", views.profile_info, name="profile_info"),
    path("change_password/<int:pk>", views.CustomPasswordChangeView.as_view(), name='password_change'),
    path("password_change_done/", views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name='password_reset'),
    path("password_reset_done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("moderation/", views.UserModerationView.as_view(), name="moderation"),
    path("moderator_edit/<int:pk>", views.UserModeratorEditView.as_view(), name="moderator_edit"),
]
