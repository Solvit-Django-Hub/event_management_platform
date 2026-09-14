from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN ="ADMIN","Admin"
        ORGANIZER="ORGANIZER","Ogranizer"
        CUSTOMER="CUSTOMER","Customer"
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.CUSTOMER)      
        
    def __str__(self):
        return self.username
class Profile(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    phone_number=models.CharField(max_length=20)
    address=models.CharField(max_length=50,blank=True)
    bio=models.TextField(blank=True)
    profile_pictue=models.ImageField(upload_to="profile/",blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return f"{self.user.username}'s Profile" 
    
