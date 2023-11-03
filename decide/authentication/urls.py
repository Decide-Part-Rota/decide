from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token


from .views import GetUserView, PersonView, LogoutView, RegisterView, loginForm, register, salir, loginForm, complete, anonymous

from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('loginForm/', loginForm),
    path('registerForm/', register),
    path('providers/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('salir/', salir, name='salir'),
    path('completeForm/', complete),
    path('anonymous/', anonymous),
    path('persons/', PersonView.as_view()),


    
]
