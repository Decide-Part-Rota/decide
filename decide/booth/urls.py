from django.urls import path
from .views import BoothView, BoothListView, BoothListPrivateView 


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('boothList/',BoothListView.as_view()),
    path('boothListPrivate/',BoothListPrivateView.as_view())
]
