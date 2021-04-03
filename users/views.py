from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from .serializers import UserSerializer
from .token import token_expire_handler
from rest_framework.response import Response

@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def login(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
    # create or get token
    token, _ = Token.objects.get_or_create(user=user)
    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)
    user_serialized = UserSerializer(user)
    return Response({
        'user': user_serialized.data,
        'token': token.key
    }, status=HTTP_200_OK)


