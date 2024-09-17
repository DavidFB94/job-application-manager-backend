from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"message": "INVALID_CREDENTIALS"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.create_user(
                username=request.data['email'],
                email=request.data['email'],
                password=request.data['password']
            )
            user.save()
            return Response({'message': 'USER_CREATED_SUCCESSFULLY'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response ({'message': 'USER_ALREADY_REGISTERD'}, status=status.HTTP_409_CONFLICT)
    return Response({'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))
