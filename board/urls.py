from django.urls import path
from .views import PostListView, PostDetailView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('posts', PostListView.as_view(), name='post-list'),
    path('posts/<int:postId>', PostDetailView.as_view(), name='post-detail'),
 
]