from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return redirect("/login/")

        try:
            validated_token = UntypedToken(token)
            user_auth = JWTAuthentication()

            try:
                user, _ = user_auth.get_user(validated_token), validated_token
            # User doesn't exist
            except AuthenticationFailed:
                response = HttpResponseRedirect("/login/")
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")
                return response

            request.user = user

        # Invalid token
        except (InvalidToken, TokenError):
            response = HttpResponseRedirect("/login/")
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response

        return view_func(request, *args, **kwargs)

    return wrapper
