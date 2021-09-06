from django.shortcuts import render

def card_swicth(request):
    return render(request, 'card/card.html')