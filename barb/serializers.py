from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email','groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id', 'name', 'desc', 'SKU', 'price', 'product_category_id', 'product_gender_id', 'discount_id', 'created_at', 'modifed_at']