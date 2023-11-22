from rest_framework import serializers

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = "src", "alt"

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializerRead(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = "fullName", "email", "phone", "avatar"


class ProfileSerializerWrite(ProfileSerializerRead):
    class Meta:
        model = Profile
        fields = "fullName", "email", "phone"


class PasswordUpdateSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)


class AvatarUpdateSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)
