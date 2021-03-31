from rest_framework.authtoken.models import Token

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

"""
	https://medium.com/@yerkebulan199/django-rest-framework-drf-token-authentication-with-expires-in-a05c1d2b7e05
"""
#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    # return expires_in(token) < timedelta(seconds = 0)
	return False # use ^^ when using tokens

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token = refresh_token(token)
    return is_expired, token

"""
	creates a new token given an old one
"""
def refresh_token(token):
	token.delete()
	token = Token.objects.create(user = token.user)
	return token

"""
	expires a given token
"""
def force_token_expiration(token):
	token.created = timezone.now() - timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS)
	token.save()