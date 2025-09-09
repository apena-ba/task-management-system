from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()

def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return redirect("/login/")
        
        try:
            validated_token = UntypedToken(token)
            user_auth = JWTAuthentication()
            user, _ = user_auth.get_user(validated_token), validated_token
            request.user = user
        except (InvalidToken, TokenError):
            return redirect("/login/")
        
        return view_func(request, *args, **kwargs)
    return wrapper
