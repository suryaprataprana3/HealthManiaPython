import traceback
from django.utils.timezone import now, timedelta
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, Application, RefreshToken

# Add usertype field in oauth2 in AccessToken Model Class library 
def get_access_token(user):

    try:
        app = Application.objects.get(user=user)
    except Application.DoesNotExist:
        app = Application.objects.create(user=user)
        pass        
    token = generate_token()
    refresh_token = generate_token()
    expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"
    access_token = AccessToken.objects.create(user=user,
                                            application=app,
                                            expires=expires,
                                            token=token,
                                            scope=scope,
                                            )
    print("access token ------->", access_token)
    RefreshToken.objects.create(user=user,
                                application=app,
                                token=refresh_token,
                                access_token=access_token
                                )
    response = {
        'access_token': access_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'refresh_token': access_token.refresh_token.token,
        'client_id': app.client_id,
        'client_secret': app.client_secret
        }
    return response

