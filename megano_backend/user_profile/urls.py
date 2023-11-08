from django.urls import path
from user_profile.views import ProfileView, SignInView, SignUpView, SignOutView, UpdatePasswordView, UpdateAvatarView

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="registration"),
    path("sign-out", SignOutView.as_view(), name="exit"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/password/', UpdatePasswordView.as_view(), name='update-password'),
    path('profile/avatar/', UpdateAvatarView.as_view(), name='update-avatar'),
]
