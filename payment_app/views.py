from django.shortcuts import redirect, render, HttpResponseRedirect
from .forms import BillingForm
from .models import BillingAddress
from order_app.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# for payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket

# Create your views here.

@login_required
def check_out(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request, "Address has been saved!!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'payment_app/checkout.html', {'form': form, 'order_items':order_items, 'order_total': order_total, 'saved_address': saved_address})

@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, "Please complete shipping address!!")
        return redirect('payment_app:checkout')
    
    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete your profile details")
        return redirect('login_app:profile')
    
    return render(request, 'payment_app/payment.html', {})