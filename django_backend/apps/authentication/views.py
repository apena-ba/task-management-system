import requests
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


User = get_user_model()


# Route   -> /api/auth/register/
# Methods -> POST
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# Route   -> /api/auth/login/
# Methods -> POST
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Route   -> /api/auth/refresh/
# Methods -> POST
class RefreshView(TokenRefreshView):
    pass


# Route   -> /api/auth/logout/
# Methods -> POST
class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."})
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_404_NOT_FOUND)


# Route   -> /logout/
class LogoutRedirectView(View):
    def get(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            response = requests.post(
                request.build_absolute_uri("/api/auth/logout/"),
                json={"refresh": refresh_token},
            )

        response = redirect("login")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response