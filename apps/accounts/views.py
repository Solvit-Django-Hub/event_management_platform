from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]
    
class LoginView(APIView):
    permission_classes=[AllowAny]
    
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
   