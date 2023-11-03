from django.contrib.auth.backends import ModelBackend

from base import mods
from django.contrib.auth.models import User



class AuthBackend(ModelBackend):
    '''
    This class makes the login to the authentication method for the django
    admin web interface.

    If the content-type is x-www-form-urlencoded, a requests is done to the
    authentication method to get the user token and this token is stored
    for future admin queries.
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):


        if '@' in username:
            print('Este es el username' + User.objects.get(email=username).username)
            username = User.objects.get(email=username).username

        u = super().authenticate(request, username=username,
                                 password=password, **kwargs)
        print('Inciando sesion')

        # only doing this for the admin web interface
        if u and request.content_type == 'application/x-www-form-urlencoded':
            data = {
                'username': username,
                'password': password,
            }
            token = mods.post('authentication', entry_point='/login/', json=data)
            request.session['auth-token'] = token['token']

        return u

