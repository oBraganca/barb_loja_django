from django.urls import path, include

app_name = "carts"

from .views import (
                        cart_detail, 
                        cart_update,
                        checkout_home, 
                    )

urlpatterns = [
    path('', cart_detail, name='home'),
    path('checkout/', checkout_home, name='checkout'),
    path('update/', cart_update, name='update'),
    path('checkout/payment', include('card.urls')),
]