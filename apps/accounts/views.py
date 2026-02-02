from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    UserUpdateSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user' : UserProfileSerializer(user).data,
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
            'message' : 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        refresh = RefreshToken.for_user(request.user)

        return Response({
            'user' : UserProfileSerializer(request.user).data,
            'refresh' : str(refresh),
            'access' : str(refresh.access_token),
            'message' : 'User registered successfully'
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user
    

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == "PATCH":
            return UserUpdateSerializer
        else:
            return UserProfileSerializer
        

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'password changed'}, status=status.HTTP_200_OK)


@api_view
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blask_list()
            return Response({"message": 'saccessfull logout'}, status=status.HTTP_200_OK)
    except:
        return Response({"error": 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
