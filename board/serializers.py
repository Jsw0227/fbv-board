from rest_framework import serializers
from .models import Board, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 또는 user.username 등

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
        
        
class BoardSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True, source='comment_set')
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'writer', 'content', 'regdate', 'readcount', 'comment']
       