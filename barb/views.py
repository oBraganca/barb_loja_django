# SERIALIZER API

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, ProductSerializer
from django.http import Http404
from .models import *



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def get(self, request, format=None):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def get(self, request, format=None):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, format=None):
    #     serializer = self.serializer_class(self.queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductViewSet(generics.RetrieveAPIView):
#     queryset = product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]
    # def get_object(self, pk):
    #     try:
    #         return self.queryset.get(pk=pk)
    #     except product.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = self.serializer_class(product)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = self.serializer_class(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# # # # # # 
from django.db.models.enums import Choices
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse,HttpResponseRedirect
from .models import product, gender, category
from .form import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.template.loader import render_to_string
import requests
import os
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

from cart.models import Cart
def index(request):
    mais_vend = product.objects.all().order_by("-vendido")[1:9].values()
    
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        "product":mais_vend,
        "cart":cart_obj,
    }
    return render(request, 'barb/index.html', context)

def allProds(request):
    search = request.GET.get('search')
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    
    
    categorys = category.objects.all()
    genders = gender.objects.all()
    proda = 9

    products= product.objects.all().order_by('-id')
        
    obj_paginator = Paginator(products, proda)
    products = obj_paginator.page(1).object_list
    page_range = obj_paginator.page_range

    
    end = obj_paginator.num_pages


    # FILTRAGEM E PAGINAÇÃO
    if request.is_ajax():
        

        categor = request.GET.getlist('category')
        gender = request.GET.getlist('gender')
        if search:
            products = product.objects.filter(title__icontains=search)
        else:
            products= product.objects.all().order_by('-id')
        if len(categor) > 0:
            for x in categor:
                products = products.filter(category=x).distinct()
        if len(gender) > 0:
            for x in gender:
                products = products.filter(gender=x).distinct()
        obj_paginator = Paginator(products, proda)
        end = obj_paginator.num_pages
        page_range = obj_paginator.page_range
        if request.GET.get('page'):
            p = int(request.GET.get('page'))
        else:
            p = 1
        products = obj_paginator.page(p).object_list

        return render(request, 'barb/product-list.html', 
        {'products': products,'genders': genders, 'categorys': categorys, 'page_range':page_range,'cart':cart_obj,'page_atual':p, 'end':end, 'prox':p+1, 'prev':p-1})
    else:
        
        return render(request, 'barb/allprods.html', 
        {'products': products,'genders': genders, 'categorys': categorys, 'page_range':page_range,'cart':cart_obj,'page_atual':1, 'end':end, 'prox':2, 'prev':1})


def viewproducts(request, id):
    prod = get_object_or_404(product, pk=id)
    # Calculo do frete

    if request.method == 'POST':
        form = calcFret(request.POST)
        if form.is_valid():

            cep = form.cleaned_data['cep']
            cep = cep.replace("-", "")

            req = requests.get("https://viacep.com.br/ws/{}/json/".format(cep))

            address_data = req.json()

            if 'erro' not in address_data:
                messages.success(request, 'Frete calculado com sucesso')
                
            else:
                messages.warning(request, 'CEP não encontrado')

            return HttpResponseRedirect('/view/{}'.format(id))
        # Termino frete
    else:
        form =  calcFret()
    
    return render(request, 'barb/viewprod.html', {'prod':prod, 'form': form})

    


def post_new(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProdForm(request.POST, request.FILES)
            if form.is_valid():
                prod = form.save(commit=False)
                prod.user = request.user
                prod.save()
                return redirect('/')
        else:
            form = ProdForm()
            return render(request, 'barb/addprod.html', {'form': form})
    else:
        return redirect('/')

def editProd(request, id):
    if request.user.is_superuser:
        prod = get_object_or_404(product, pk=id)
        form = ProdForm(instance=prod)
        if(request.method == 'POST'):
            form = ProdForm(request.POST, request.FILES, instance=prod)
            
            if(request.FILES):
                    old_img = str(prod.upload)
            
            if(form.is_valid()):
                if 'old_img' in locals() or 'old_img' in globals():
                    default_storage.delete(old_img)
                prod.save()
                
                return redirect('/')
            else:
                return render(request, 'barb/editprod.html', {'form': form, 'prod': prod})
        else:
            return render(request, 'barb/editprod.html', {'form': form, 'prod': prod})
    else:
        return redirect('/')


def deleteProd(request, id):
    if request.user.is_superuser:
        prod = get_object_or_404(product, pk=id)
        default_storage.delete(str(prod.upload))
        prod.delete()
    else:
        return redirect('/')

    return redirect('/')




