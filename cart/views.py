from django.db.models.fields import DecimalField
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, Qnty
from orders.models import Order

from accounts.forms import LoginForm
from billing.models import BillingProfile

from django.contrib import messages

from barb.models import product

from decimal import Decimal

def cart_detail(request):
    cart_obj, new_obj  = Cart.objects.new_or_get(request)
    

    pro = Qnty.objects.all()
    pri = cart_obj.products.all()

    if pro:
        for qnt_cart in pro:
            if qnt_cart.cart == cart_obj :
                if not pri:
                    qnt_cart.delete()
    
    else:
        for i in pri:
            Qnty.objects.create(cart = cart_obj, products=i)


    # for p in pro:
    #     if p.qnty > p.products.amount:
    #         if p.cart == cart_obj:
    #             print(p.id,'----',p.products.amount)
    #             messages.error(request, 'Essa quantidade não está disponivel')
    
    if request.is_ajax():
        for i in pro:
            a = request.GET.get(f'{str(i)}')

            b = request.GET.get('click')

            try:
                if len(a) > 0:
                    if int(a) <= i.products.amount:
                        if str(i) == b:
                            i.qnty = a
                            i.total = round(Decimal(i.qnty) * Decimal(i.products.price),2)
                            i.save()
                            return JsonResponse({'data' : float(i.total), 'id' : str(i)})
                    else:
                        print("Esse produto está esgotado/nao disponivel para essa quantidade de compra")
            except Exception as e:
                print(e)
                pass
        

    if pro:
        context={
            "cart": cart_obj,
            'pro':pro
        }
    else:
        context={
            "cart": cart_obj
        }

    return render(request, 'cart/cart_detail.html',  context)

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = product.objects.get(id = product_id)
        except product.DoesNotExist:
            print("Mostrar mensagem ao usuário, esse produto acabou!")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all(): 
            cart_obj.products.remove(product_obj)
            Qnty.objects.filter(products=product_obj).delete()
        else: 
            cart_obj.products.add(product_obj)
            Qnty.objects.create(cart = cart_obj, products=product_obj, total = product_obj.price) #Coloca o produto clicado no Qnty
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")

def checkout_home(request):
    #aqui a gente pega o carrinho
    cart_obj, cart_created= Cart.objects.new_or_get(request)
    order_obj = None
    #se o carrinho acabou de ser criado, ele tá zerado
    #ou se o carrinho já existir mas não tiver nada dentro
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    #aqui a order associada ao carrinho
    else:
        
        order_obj, new_order_obj = Order.objects.get_or_create(cart = cart_obj)
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user = user, email = user.email)
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form ": login_form 
    }
    return render(request, "cart/checkout.html",context)

# def qnt_prod(request):
#     for i in request.GET.keys():
#         a = [request.GET.get(f'{str(i)}')]

#     print(a)