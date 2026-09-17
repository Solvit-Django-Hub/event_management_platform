
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer,ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]
    
class LoginView(APIView):
    permission_classes=[AllowAny]
    
    @extend_schema(
    request=LoginSerializer,responses=200,)
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
    
    @extend_schema(
    request=LogoutSerializer,responses=200,)
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
    
    @extend_schema(
    responses=ProfileSerializer,)
    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @extend_schema(
    request=ProfileSerializer,responses=200,)
    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile,data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(
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
    
    @extend_schema(
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
    