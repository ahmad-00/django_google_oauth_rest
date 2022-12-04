import hashlib
import os


def generate_url(request, setting) -> str:
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session['state'] = state

    token_request_uri = getattr(setting, "TOKEN_REQUEST_URI", "https://accounts.google.com/o/oauth2/auth")
    response_type = "code"
    client_id = getattr(setting, "CLIENT_ID")
    redirect_uri = getattr(setting, "REDIRECT_URI")
    scope = getattr(setting, "SCOPE", "email profile")
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&state={state}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri=token_request_uri,
        response_type=response_type,
        client_id=client_id,
        state=state,
        redirect_uri=redirect_uri,
        scope=scope)
    return url
