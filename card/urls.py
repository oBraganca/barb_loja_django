from django.urls import path, include
from card import views
app_name = "cards"

urlpatterns = [
    path('', views.card_swicth, name='card_swicth'),
]