from rest_framework import serializers
from .models import Blog
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.db.models import fields

class formserializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())],required=True,max_length=32)
    password = serializers.CharField(min_length=6)

    def create(self,validate_data):
        user = User.objects.create_user(validate_data['username'],validate_data['email'],
            validate_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id','email','username','password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id','Blog_title','blog_desc','short_content','user')
