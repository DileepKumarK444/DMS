from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


class CustomAuthToken(ObtainAuthToken):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        token = self.token_expire_handler(token)
        return Response({'token': token.key})

    @staticmethod
    def expires_in(token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(
            seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user=token.user)
        return token


obtain_auth_token = CustomAuthToken.as_view()