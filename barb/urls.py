from django.urls import path, include
from cart.views import cart_detail
from rest_framework import routers
from . import views

from accounts.views import login_page, register_page
from django.contrib.auth.views import LogoutView 


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='UserView')
router.register(r'groups', views.GroupViewSet, basename='GroupView')
router.register(r'products', views.ListProductsViewSet, basename='ProductsView')
router.register(r'product/<int:pk>', views.ProductViewSet, basename='ProductView')

urlpatterns = [
    path('', include(router.urls)),
    # path('', views.index, name='index'),
    # path('prods/', views.allProds, name='allprods'),
    # path('view/<int:id>', views.viewproducts, name='view-product'),
    # path('newprod/',views.post_new, name='new-prod'),
    # path('edit/<int:id>', views.editProd, name='edit-product'),
    # path('delete/<int:id>', views.deleteProd, name='delete-Prod'),
    # path('cart/', include("cart.urls", namespace="cart")),
    # path('login/', login_page, name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', register_page, name='register'),
]
    