import json

import jwt
import requests
from django.conf import LazySettings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View

from google_auth.generate_url import generate_url

User = get_user_model()


class AuthURL(View):

    def post(self, request):
        return HttpResponseRedirect(generate_url(request=request, setting=_setting))

    def get(self, request):
        return JsonResponse(
            {
                "url": generate_url(request=request, setting=_setting)
            }
        )


class AuthCallback(View):
    def get(self, request):
        validate_state = getattr(_setting, 'VALIDATE_STATE', True)
        if validate_state:
            if request.GET.get('state', '') != request.session['state']:
                return JsonResponse(
                    {
                        "message": "Invalid state parameter"
                    }
                ), 401

        user_info_request_uri = getattr(_setting, "USER_INFO_REQUEST_URI", "https://oauth2.googleapis.com/token")
        client_id = getattr(_setting, "CLIENT_ID")
        client_secret = getattr(_setting, "CLIENT_SECRET")
        code = request.GET.get('code')
        redirect_uri = getattr(_setting, "REDIRECT_URI")
        payload = f'code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", user_info_request_uri, headers=headers, data=payload)
        try:
            content = response.content
            json_content = json.loads(content)
            id_token = json_content['id_token']
        except:
            return JsonResponse(
                {
                    "message": "Verification failed"
                }
            ), 401

        payload = jwt.decode(id_token, options={"verify_signature": False})

        email = payload['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User(
                email=email,
                given_name=payload['given_name'],
                family_name=payload['family_name']
            )
            set_register_user_field = getattr(_setting, "SET_REGISTER_USER_FIELD", {})
            for k, v in set_register_user_field.items():
                setattr(user, k, v)
            user.save()
        except Exception:
            return JsonResponse(
                {
                    "message": "Server Error"
                }
            ), 500

        return user


_setting = LazySettings()
