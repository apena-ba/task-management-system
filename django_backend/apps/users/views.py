from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer


# Route   -> /api/users/
# Methods -> GET
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Route   -> /api/users/{id}/
# Methods -> GET PUT
class UserDetailsView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "put"]  
    permission_classes = [permissions.IsAuthenticated]

# Route   -> /api/users/me/
# Methods -> GET
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
