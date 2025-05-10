from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer


class UserCreateSerializer(DjoserUserCreateSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta(DjoserUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "password2",
        ]
        ref_name = "CustomUserCreateSerializer"

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "رمز عبور با تکرار آن مطابقت ندارد"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        return super().create(validated_data)

    

class UserSerializer(DjoserUserSerializer):

    class Meta(DjoserUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]
        read_only_fields = ["id"]
        ref_name = "CustomUserSerializer"
