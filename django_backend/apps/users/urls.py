from django.urls import path
from .views import UserListView, UserDetailsView, MeView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailsView.as_view(), name="user-detail"),
    path("users/me/", MeView.as_view(), name="user-me"),
]
