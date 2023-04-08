from rest_framework.serializers import ModelSerializer
from .models import Tasks
from django.contrib.auth.models import User

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id','assigned','name','category','location','created','image','approved']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
