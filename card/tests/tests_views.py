from barb.models import product
from django.test import TestCase, Client, client
from cart.models import Cart, Qnty
from barb.models import product, category, gender 
import pagarme

from django.urls import reverse


from django.contrib.auth.models import User

# Create your tests here.

class TestTemplate(TestCase):
    def test_card_index(self):
        c =Client()
        response = c.get('/cart/checkout/payment', follow=True)
        self.assertEqual(response.status_code, 200)

class TestCardTransationView(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user('Payment1', 'payment1@chase.com', 'payment1password')
        self.category = category.objects.create(category ='oa')
        self.gender = gender.objects.create( gender = 'F')

        self.prod1 = product.objects.create(
            title = 'prod1', description= 'prod', price = 212, amount = 55, upload = 'a/a/a/',
            category = self.category, gender = self.gender, vendido = 45
            )
        self.prod2 = product.objects.create(
            title = 'prod2', description= 'prod', price = 212, amount = 55, upload = 'a/a/a/',
            category = self.category, gender = self.gender, vendido = 45
            )
        self.prod3 = product.objects.create(
            title = 'prod3', description= 'prod', price = 212, amount = 55, upload = 'a/a/a/',
            category = self.category, gender = self.gender, vendido = 45
            )
            
        self.cart1 = Cart.objects.create(user = self.user_1)
        self.cart1.products.set([x for x in product.objects.all()])

        for x in self.cart1.products.all():
            self.qnty = Qnty.objects.create(cart = self.cart1, products=x, qnty = 3, total=x.price * 3)



    def test_transation(self):
        pro = Qnty.objects.all()

        total_cart = 0
        for x in pro:
            total_cart += x.total
        total_cart = int(total_cart)*100
        items=[]
        for x in pro.values():
            x['id'] = str(x['id'])
            x['total'] = int(x['total'])
            x['title'] = str(x['products_id'])
            x['unit_price'] = (int(x['total']) / int(x['qnty']))*100
            x['quantity'] = int(x['qnty'])
            x['tangible'] = True
            x.pop('cart_id')
            x.pop('products_id')
            x.pop('qnty')
            x.pop('total')
            items.append(x)

        pagarme.authentication_key('ak_test_wdvOicpMKVHtIJ3aTnER2aj24U6h6s')
        
        params = {
            "amount": total_cart,
            "card_number": "4111111111111111",
            "card_cvv": "123",
            "card_expiration_date": "0922",
            "card_holder_name": "Thayllon Ryan",
            "customer": {
            "external_id": "#3311",
            "name": "Thayllon Ryan",
            "type": "individual",
            "country": "br",
            "email": "thayllon@nabucodonozor.com",
            "documents": [
                {
                "type": "cpf",
                "number": "70430967667"
                }
            ],
            "phone_numbers": ["+5511999998888", "+5511888889999"],
            "birthday": "2003-01-29"
            },
            "billing": {
                "name": "Trinity Moss",
                "address": {
                    "country": "br",
                    "state": "sp",
                    "city": "Cotia",
                    "neighborhood": "Rio Cotia",
                    "street": "Rua Matrix",
                    "street_number": "9999",
                    "zipcode": "06714360"
                }
            },
            "shipping": {
                "name": "Neo Reeves",
                "fee": "1000",
                "delivery_date": "2000-12-21",
                "expedited": True,
                "address": {
                    "country": "br",
                    "state": "sp",
                    "city": "Cotia",
                    "neighborhood": "Rio Cotia",
                    "street": "Rua Matrix",
                    "street_number": "9999",
                    "zipcode": "06714360"
                }
            },
            "items":
                items
                
        }

        pagarme.transaction.create(params)


