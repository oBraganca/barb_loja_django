from barb.models import product
from django.test import TestCase, Client, client
from cart.models import Cart, Qnty
from barb.models import product, Category, Gender 
import pagarme

from django.urls import reverse


from django.contrib.auth.models import User

class TestExcludeImage(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category ='oa')
        self.gender = Gender.objects.create( gender = 'F')

        self.prod1 = product.objects.create(
            title = 'prod1', description= 'prod', price = 212, amount = 55, upload = 'a/a/a/',
            category = self.category, gender = self.gender, vendido = 45
            )
            
        # self.cart1 = Cart.objects.create(user = self.user_1)
        # self.cart1.products.set([x for x in product.objects.all()])

        # for x in self.cart1.products.all():
        #     self.qnty = Qnty.objects.create(cart = self.cart1, products=x, qnty = 3, total=x.price * 3)
    
    # def test_return_image(self):
    #     print(self.prod1.upload.delete(),'aa')
    #     print(self.prod1.upload)
    #     # print(self.prod1.all())