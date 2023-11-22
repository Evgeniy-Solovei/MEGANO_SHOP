import json

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.models import Profile
from user_profile.serializers import (AvatarUpdateSerializer,
                                      PasswordUpdateSerializer,
                                      ProfileSerializerRead,
                                      ProfileSerializerWrite)


class SignInView(APIView):
    """Класс для входа пользователей"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    """Класс для регистрации пользователя"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(request.body)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignOutView(APIView):
    """Выход пользователя"""

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status=status.HTTP_200_OK)


# class ProfileView(APIView):
#     def get(self, request: Request) -> Response:
#         user = request.user.pk  # получаем user_id
#         profile = Profile.objects.get(user_id=user)  # выбираем конкретный авторизованный профиль
#         serialized = ProfileSerializer(profile, many=False)  # сериализуем
#         return Response(serialized.data)
#
#     def post(self, request: Request) -> Response:
#         data = request.data  # получаем данныe из запроса
#         user = request.user.pk  # получаем id  авторизованного пользователя
#         profile = Profile.objects.get(user_id=user)  # получаем авторизованного пользователя
#         serialized = ProfileSerializer(profile, many=False)
#         profile.fullName = data['fullName']  # обновляем все поля профиля из данных, введённых в форму
#         profile.phone = data['phone']
#         profile.email = data['email']
#         profile.save()  # сохраняем экземпляр в  базу данных
#         return Response(serialized.data)


class ProfileView(APIView):
    """Класс для получения информации о пользователе (get), редактирования информации о пользователе (post)"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serialized = ProfileSerializerRead(profile)
        return Response(serialized.data)

    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializerWrite(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    """Смена пароля пользователя"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateSerializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data.get("currentPassword")
            new_password = serializer.validated_data.get("newPassword")

            user = request.user
            user.set_password = new_password
            user.save()
            update_session_auth_hash(request, user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAvatarView(APIView):
    """Смена аватара пользователя"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        avatar_img = request.FILES["avatar"]

        if avatar_img:
            profile_avatar, created = Profile.objects.get_or_create(user=request.user)
            profile_avatar.src = avatar_img
            profile_avatar.save()
            return Response(
                {"detail": "Аватар успешно обновлен"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Файл аватара не найден"}, status=status.HTTP_400_BAD_REQUEST
            )
