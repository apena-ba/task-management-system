from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


# List all users with pagination
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Retrieve a user by ID
class UserDetailsView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "put"]  
    permission_classes = [permissions.IsAuthenticated]

# Get currently authenticated user
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
