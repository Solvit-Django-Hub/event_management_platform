from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = {
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role"
        }        

    def create(self, validated_data):
        validated_data["Role"]=User.Role.CUSTOMER
        user = User.objects.create_user(**validated_data)

        # New accounts must be activated through email
        user.is_active = False
        user.save(update_fields=["is_active"])

        Profile.objects.create(
            user=user,
            phone_number=""
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid name or password"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Please activate your account through your email before logging in."
            )

        data["user"] = user
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        try:
            token = RefreshToken(data["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )

        return data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )
    first_name = serializers.CharField(
        source="user.first_name"
    )
    last_name = serializers.CharField(
        source="user.last_name"
    )
    role = serializers.CharField(
        source="user.role",
        read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "address",
            "bio",
            "profile_picture",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "role",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        user = instance.user

        for field, value in user_data.items():
            setattr(user, field, value)

        user.save()

        return super().update(
            instance,
            validated_data
        )


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user

        if not user.check_password(
            data["current_password"]
        ):
            raise serializers.ValidationError({
                "current_password":
                    "Current password is incorrect."
            })

        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password":
                    "Passwords do not match."
            })

        return data

    def save(self):
        user = self.context["request"].user

        user.set_password(
            self.validated_data["new_password"]
        )
        user.save()

        return user


class ActivateAccountSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )
    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password":
                    "Passwords do not match."
            })

        return data