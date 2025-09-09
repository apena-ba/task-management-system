from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.authentication.views import LogoutRedirectView
from apps.tasks.views import (
    TaskListView,
    TaskDetailTemplateView,
    TaskCreateTemplateView,
    ReportsTemplateView,
    ReportDownloadView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirects
    path('', lambda request, **kwargs: redirect('tasks'), name="root"),

    # API routes
    path("api/auth/", include("apps.authentication.urls")),
    path("api/", include("apps.users.urls")),
    path("api/", include("apps.tasks.urls")),

    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Template routes
    path("login/", lambda request: render(request, "login.html"), name="login"),
    path("register/", lambda request: render(request, "register.html"), name="register"),
    path("logout/", LogoutRedirectView.as_view(), name="logout"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/create/", TaskCreateTemplateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailTemplateView.as_view(), name="task-detail"),
    path("reports/", ReportsTemplateView.as_view(), name="reports"),
    path("reports/download/<str:filename>/", ReportDownloadView.as_view(), name="report-download"),
]
