from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login,logout,authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import JSONParser
from .models import Blog
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import formserializers,UserSerializer

# rest framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class RegisterAPI(APIView):
    def post(self,request):
        serializer=formserializers(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            if user:
               token = RefreshToken.for_user(user)
               user_data = serializer.data
               #user_data.pop('password')
               
            return Response(data={"username":user_data['username'],"token":str(token.access_token)},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
class Login(APIView):
    def post(self,request):
       
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token = RefreshToken.for_user(user)
                response_serializer=formserializers(user)
                return Response(data={"username": username, "token":str(token.access_token) ,"success":"welcome,Login Successfully!"},status=status.HTTP_200_OK)
            else:
                return Response(data={'password': 'Password is Incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(data={'username': "User with this Username doesn't exist"},
            status=status.HTTP_401_UNAUTHORIZED)
class LogoutAPI(APIView):
    def get(self,request):
        logout(request)
        return Response({"message":"Logout Successfully"})
        

class BlogAPI(APIView):
    permission_classes = [AllowAny] 
    def get(self,request):
        blog = Blog.objects.all()
        serializer=UserSerializer(blog,many=True)
        return Response(serializer.data)
    
class UserblogAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,blog_id=None):
        user =request.user
        if blog_id:
            try:
                blog = Blog.objects.get(id=blog_id,user=user)
                serializer=UserSerializer(blog)
                return Response(serializer.data)
            except:
                return Response("Blog Not present")
        else:
            user =request.user
            userblog = Blog.objects.filter(user=user)
            serializer=UserSerializer(userblog,many=True)
            
            return Response(serializer.data)
    
    def post(self,request):
        data = JSONParser().parse(request)
        title=data['Blog_title']
        desc=data['blog_desc']
        headline=data['short_content']
        user = request.user
        blog,create = Blog.objects.get_or_create(
            Blog_title = title,blog_desc= desc,short_content=headline,
            user = request.user)
        if create:
            return Response("Blog added")
        return Response("Blog alredy present")

    def put(self,request):
        data=JSONParser().parse(request)
        id = data['id']
        title=data['Blog_title']
        desc=data['blog_desc']
        headline=data['short_content']
        user = request.user
        try:
            blog=Blog.objects.get(id=id,user=user)
        except:
            return Response({"message":"This Blog not found for this user"})
        if blog:
            if title:
                    blog.Blog_title = title
            if desc:
                blog.blog_desc = desc
            if headline:
                blog.short_content = headline
            blog.save()
            return Response({"message":"Blog updated Successful"})
    
    def delete(self,request,blog_id=None):
        try:
            Blog.objects.get(
                id=blog_id,
                user=request.user
            ).delete()
        except:
            return Response({"message":"Blog not found for this user"})
        return Response({"message":"Blog deleted"})