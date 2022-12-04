**Django Google Auth**
======================

This project help with Google Authentication flow when you prefer API
approach. It uses existing User model in your database and no other
tables are created. It also lets you modify parameters based on your
business logic and current authentication flow.

**Quick Start**
---------------

1. Add “google_auth” to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'google_auth',
    ]

2. Add “email” field to your user table if it doesn’t already exist.

3. (OPTIONAL) To have user retrieved info saved in your add these fields
   to your user table:

   -  given_name
   -  family_name

4. Add a new url to your projects url.py like this:

.. code-block:: python

   re_path('auth/url', views.AuthURL.as_view(), name="auth_url")

5. Create a new view which is a subclass of ‘**AuthCallback**’ like
   this:
   
.. code-block:: python

   class CallbackView(AuthCallback):
      def get(self, request):
         user = super(CallbackView, self).get(request)         
         # create new token and authenticate user. Return token and required parameters here``

6. Add another new url to your projects url.py like this:

.. code-block:: python

   re_path('auth/calback', views.CallbackView.as_view(), name="auth_calback_url")

**Configuration parameter**
---------------------------

-  AUTH_USER_MODEL: Authentication user table in your models
-  CLIENT_ID: Retrieved from Google console
-  CLIENT_SECRET: Retrieved from Google console
-  REDIRECT_URI: Redirect url same as redirect url in google console
   (Usually it should route to your front-end url)
-  VALIDATE_STATE: (OPTIONAL) state is a server side generated security
   feature suggested by google. It will be saved in session. default
   value it True. If set to False it will bypass this security check.
-  SET_REGISTER_USER_FIELD: (OPTIONAL) If you want to set some value in
   User table after login/register process is successful, you can set it
   here. In example below, we set user verified field to True when
   login/register process is successful:
   
   .. code-block:: python
   
      SET_REGISTER_USER_FIELD = {
        "verified": True
      }
      
-  USER_INFO_REQUEST_URI: (OPTIONAL) Google verification url. Should be
   fine with default value.

**URLs Flow**
--------------

1. First call ‘auth/url’ by POST(Empty body) or GET Method.

   -  GET method will return generated URL in JSON response. Your front
      end should redirect to this URL.
   -  POST method will return 302 status code with redirect url.

2. After redirecting to received URL from step 1, user can verify from
   Google. If verification is successful Google will call your
   redirect_uri.
3. when redirect_uri is called your frontend should call the Callback
   url you already created (step 6 in Quick start).

   -  IMPORTANT: You must add all query params received from Google in
      this step to ‘auth/callback’ as query params.