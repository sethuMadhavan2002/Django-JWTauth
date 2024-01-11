from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from werkzeug.security import generate_password_hash
from .serializers import UserSerializers

from .models import User
import jwt, datetime


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginUser(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        access_payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            "iat": datetime.datetime.utcnow(),
        }

        refresh_payload = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        }

        access_token = jwt.encode(access_payload, "anybodycancode", algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, "anybodycancode", algorithm="HS256")

        response = Response()

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        response.data = {"message": "logged in", "token": access_token}

        return response


class RefreshApi(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token is None:
            raise AuthenticationFailed("unauthenticated")
        data = jwt.decode(refresh_token, "anybodycancode", algorithms=["HS256"])
        access_payload = {
            "id": data["id"],
            "email": data["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            "iat": datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_payload, "anybodycancode", algorithm="HS256")
        response = Response()
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return Response({"access_token": access_token})


class UserView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            access_token = auth[1]

            if not access_token:
                raise AuthenticationFailed("unauthenticated")

            try:
                payload = jwt.decode(
                    access_token, "anybodycancode", algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("unauthenticated")

            user = User.objects.get(id=payload["id"])

            serializer = UserSerializers(user)

            return Response(serializer.data)
        return AuthenticationFailed("unauthenticated")


class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.data = {"message": "Logged out"}
        return response
