from django.urls import path
from .views import RegisterAPI,Login,BlogAPI,LogoutAPI,UserblogAPI

urlpatterns = [
    path('register/',RegisterAPI.as_view(), name="register"),
    path('login/',Login.as_view(), name="login"),
    path('logout/',LogoutAPI.as_view(), name="logout"),
    path('blog/',BlogAPI.as_view(), name="blog"),
    path('user_blog/',UserblogAPI.as_view(), name="user_blog"),
    path('user_blog/<int:blog_id>',UserblogAPI.as_view(), name="user_blog"),
    
]
