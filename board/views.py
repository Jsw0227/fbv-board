from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoardSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Board


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_summary="회원가입",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username','email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: '회원가입 성공', 400: '잘못된 요청'},
    )
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            user.save()
            return JsonResponse({"userId": user.id, "token": "dummy-token"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="로그인",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: openapi.Response('로그인 성공', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'token': openapi.Schema(type=openapi.TYPE_STRING)}
        )), 401: '인증 실패'}
    )
    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return JsonResponse({"token": "dummy-token"}, status=200)
        return HttpResponse(status=401)

class LogoutView(APIView):
    @swagger_auto_schema(
        operation_summary="로그아웃",
        responses={200: '로그아웃 성공'}
    )
    def post(self, request):
        logout(request)
        return HttpResponse(status=200)

class PostListView(APIView):
    @method_decorator(csrf_exempt)
    @swagger_auto_schema(operation_summary="게시글 목록 조회",responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request):
        boards = Board.objects.all().order_by('-id')
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(csrf_exempt)
    @swagger_auto_schema(operation_summary="게시글 작성",request_body=BoardSerializer, responses={201: BoardSerializer, 400: 'Invalid data'})
    def post(self, request):
        title = request.data.get('title')
        writer = request.data.get('writer')
        content = request.data.get('content')
        if title and writer and content:
            board = Board.objects.create(title=title, writer=writer, content=content)
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    @swagger_auto_schema(operation_summary="게시글 검색",responses={200: BoardSerializer, 404: 'Board not found'})
    def get(self, request, postId):
        try:
            board = Board.objects.get(pk=postId)
            board.incrementReadCount()
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_summary="게시글 수정",request_body=BoardSerializer, responses={200: BoardSerializer, 404: 'Board not found'})
    def put(self, request, postId):
        try:
            board = Board.objects.get(pk=postId)
            board.title = request.data.get('title', board.title)
            board.writer = request.data.get('writer', board.writer)
            board.content = request.data.get('content', board.content)
            board.save()
            return Response({'message': 'Board updated successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="게시글 삭제", responses={200: '게시글 삭제 성공', 404: 'Board not found'})
    def delete(self, request, postId):
        try:
            board = Board.objects.get(pk=postId)
            board.delete()
            return Response({'message': 'Board deleted successfully'}, status=status.HTTP_200_OK)
        except Board.DoesNotExist:
            return Response({'error': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
        
