from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from core.utils import APIResponse
from .serializers import (
    RegisterSerializer,
    MeSerializer,
    ChangePasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                message='Registration failed',
                errors=serializer.errors,
                status_code=400
            )
        user = serializer.save()
        return APIResponse.success(
            message=f'Welcome, {user.first_name}! Your account has been created.',
            status_code=201
        )


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return APIResponse.error(
                message='Refresh token is required',
                status_code=400
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return APIResponse.success(message='Logged out successfully')
        except TokenError:
            return APIResponse.error(
                message='Invalid or expired token',
                status_code=400
            )


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class   = MeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return APIResponse.success(
            data=serializer.data,
            message='Profile retrieved successfully'
        )

    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Update failed',
                errors=serializer.errors,
                status_code=400
            )
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message='Profile updated successfully'
        )


class ChangePasswordView(generics.GenericAPIView):
    serializer_class   = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return APIResponse.error(
                message='Password change failed',
                errors=serializer.errors,
                status_code=400
            )
        serializer.save()
        return APIResponse.success(message='Password changed successfully')