from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response

from uneplan.restPermissions.roleComposeUtil import combine_arr_of_roles
from uneplan.serializers.submitSerializers import UserSerializer
from uneplan.serializers.simpleSerializers.RoleSimpleSerializer import RoleSimpleSerializer
from uneplan.view.standardRoutes.loggedInUsers.utilFuncs.tokenHandle import token_expire_handler, expires_in

"""
	https://medium.com/@yerkebulan199/django-rest-framework-drf-token-authentication-with-expires-in-a05c1d2b7e05
"""

@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def login(request):
    signin_serializer = UserSerializer(data = request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)
    user = authenticate(
        username = signin_serializer.data['username'],
        password = signin_serializer.data['password']
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
    # create or get token
    token, _ = Token.objects.get_or_create(user = user)
    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)
    user_serialized = UserSerializer(user)
    role = RoleSimpleSerializer(combine_arr_of_roles(user.roles.all()))
    return Response({
        'user': user_serialized.data,
		'role': role.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)
