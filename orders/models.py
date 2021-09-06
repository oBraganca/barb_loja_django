from django.db import models
from django.db.models.signals import pre_save, post_save

from cart.models import Cart

import random
import string
import math

ORDER_STATUS_CHOICES = (
    ('created', 'Criado'),
    ('paid', 'Pago'),
    ('shipped', 'Enviado'),
    ('refunded', 'Devolvido'),
)

class Order(models.Model):
    order_id = models.CharField(max_length = 120, blank = True)
    # billing_profile = ?
    # shipping_address = ?
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null = True)
    status = models.CharField(max_length = 120, default = 'created', choices = ORDER_STATUS_CHOICES )
    shipping_total = models.DecimalField(default = 5.99, max_digits = 100, decimal_places = 2)
    total = models.DecimalField(default = 0.00, max_digits = 100, decimal_places = 2)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total 
        self.save()
        return new_total

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    order_new_id = random_string_generator()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id = order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender = Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    print("Executando")
    if created:
        print("Atualizando")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)