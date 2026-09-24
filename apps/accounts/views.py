
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer,ChangePasswordSerializer,ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    ActivateAccountSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
# Create your views here.
"""Handles user registration."""
@extend_schema(tags=["Authentication"])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        activation_link = (
            f"http://127.0.0.1:8000/api/auth/activate/"
            f"?uid={uid}&token={token}"
        )

        send_mail(
            subject="Activate your Event Management Platform account",
            message=(
                f"Hello {user.username},\n\n"
                f"Thank you for registering with the Event Management Platform.\n\n"
                f"Please activate your account using the link below:\n\n"
                f"{activation_link}\n\n"
                f"If you did not create this account, you can ignore this email."
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
"""Handles user authentication and JWT token generation."""    
class LoginView(APIView):
    permission_classes=[AllowAny]
    
    @extend_schema(tags=["Authentication"],
    request=LoginSerializer, responses=OpenApiResponse(description="Login successful."))
    def post(self, request):
        Serializer=LoginSerializer(data=request.data)
        
        if Serializer.is_valid():
            user =Serializer.validated_data["user"]
            refresh =RefreshToken.for_user(user)
            return Response(
                {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "user":{
                        "id":user.id,
                         "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "role": user.role,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
    
           
class LogoutView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(tags=["Authentication"],
    request=LogoutSerializer,responses=OpenApiResponse(description="logout successful"))
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {"message": "Logout successful."},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    
   
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(tags=["User Management"],
    responses=ProfileSerializer,)
    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(tags=["User Management"],
    request=ProfileSerializer,responses=200,)
    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile,data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(tags=["User Management"],
    request=ProfileSerializer,responses=200,)
    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(tags=["User Management"],
    request=ChangePasswordSerializer,responses=200,)
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )    

User = get_user_model()


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ActivateAccountSerializer,
        responses=200,
    )
    def post(self, request):
        serializer = ActivateAccountSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = force_str(
                urlsafe_base64_decode(serializer.validated_data["uid"])
            )
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid activation link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = serializer.validated_data["token"]

        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "Invalid or expired activation link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save(update_fields=["is_active"])

        return Response(
            {"message": "Account activated successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses=200,
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = (
                f"http://127.0.0.1:8000/api/auth/reset-password/"
                f"?uid={uid}&token={token}"
            )

            send_mail(
                subject="Reset your Event Management Platform password",
                message=(
                    f"Hello {user.username},\n\n"
                    f"Use the link below to reset your password:\n\n"
                    f"{reset_link}\n\n"
                    f"If you did not request this, you can ignore this email."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

        return Response(
            {
                "message": (
                    "If an account with that email exists, "
                    "a password reset link has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses=200,
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = force_str(
                urlsafe_base64_decode(serializer.validated_data["uid"])
            )
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = serializer.validated_data["token"]

        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "Invalid or expired password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response(
            {"message": "Password reset successfully. You can now log in."},
            status=status.HTTP_200_OK,
        )    