from django.urls import path
from .views import PostListView, PostDetailView, RegisterView, LoginView, LogoutView, CommentView,CommentDeleteView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('posts', PostListView.as_view(), name='post-list'),
    path('posts/<int:postId>', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:postId>/comments/', CommentView.as_view(), name='comment'),
    path('posts/<int:postId>/comments/<int:commentId>/', CommentDeleteView.as_view(), name='comment-delete'),

]