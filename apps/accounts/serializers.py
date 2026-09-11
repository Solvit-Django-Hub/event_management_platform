from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    
    class Meta:
        model=User
        fields='__all__'
        read_only_fields=["id"]
        
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        
        return user    
    
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)
    
    def validate(self, data):
        username=data.get("username")
        password=data.get("password")
        
        user =authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid name or password")
        if not user.is_active:
            raise serializers.ValidationError("This account is not active") 
        data["user"]=user
        return data
class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()
    
    def validate(self,data):
        try:
            token=RefreshToken(data["refresh"])
            token.blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid or expired referesh token.")
        return data    