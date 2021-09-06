from django.test import TestCase, Client
from cart.models import Cart

class TestManagerSession(TestCase):
    def setUp(self):
        self.c = Client()
        self.response = self.c.get('/cart')
        
    def test_session_ok(self):
        print(Cart.objects.all().values())