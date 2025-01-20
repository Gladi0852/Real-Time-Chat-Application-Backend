from channels.middleware import BaseMiddleware
from rest_framework.exceptions import AuthenticationFailed
from django.db import close_old_connections
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class TokenAuthenticatorMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()  

        # Extracting query
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(qs.split("=") for qs in query_string.split("&"))
        token = query_parameters.get("token", None)

        
        if token is None:
            await send({
                "type": "websocket.close",
                "code": 4000  
            })
            return

        try:
            # Use sync_to_async to run the database query in an async
            user = await self.get_user_from_token(token)
            if user is None:
                raise AuthenticationFailed("Invalid token")
            
            scope['user'] = user
            await super().__call__(scope, receive, send)
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid token")
        except Exception as e:
            
            print(f"Unexpected error during authentication: {str(e)}")
            raise AuthenticationFailed("An error occurred during authentication")

    # get user from the token asynchronously
    @sync_to_async
    def get_user_from_token(self, token):
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user  
        except Token.DoesNotExist:
            return None
