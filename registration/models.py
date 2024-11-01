from django.db import models
from django.contrib.auth.models import AbstractBaseUser




class Customer(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    date_joined = models.DateTimeField(auto_now_add=True)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.email

