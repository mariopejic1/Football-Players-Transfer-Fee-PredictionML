from django.urls import path
from .views import predict_home, PlayerPredictionView

urlpatterns = [
    path('', predict_home, name='home'),  
    path('app/predict/', PlayerPredictionView.as_view(), name='predict'),  
]