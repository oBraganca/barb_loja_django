from django.urls import include, path

from . import views

urlpatterns = [ 
    path('register/', views.SignUp.as_view(), name='signup'),
    
]