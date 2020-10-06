from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from .forms import BillingForm
from .models import BillingAddress
from order_app.models import Order, Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, "Please complete shipping address!!")
        return redirect('payment_app:checkout')
    
    if not request.user.profile.is_fully_filled():
        messages.info(request, "Please complete your profile details")
        return redirect('login_app:profile')

    store_id = 'thede5f74ce59e2e9c'
    API_key = 'thede5f74ce59e2e9c@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse('payment_app:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].order_items.all()
    order_items_count = order_qs[0].order_items.count()
    order_total = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    # customer info
    current_user = request.user
    mypayment.set_customer_info(
        name=current_user.profile.full_name, 
        email=current_user.email, 
        address1=current_user.profile.address_1, 
        address2=current_user.profile.address_1, 
        city=current_user.profile.city, 
        postcode=current_user.profile.zipcode, 
        country=current_user.profile.country, 
        phone=current_user.profile.phone
    )
    # shipping info
    mypayment.set_shipping_info(
        shipping_to=current_user.profile.full_name, 
        address=saved_address.address, 
        city=saved_address.city, 
        postcode=saved_address.zipcode, 
        country=saved_address.country
    )

    response_data = mypayment.init_payment()
    
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, f'Your payment completed successfully')
            return HttpResponseRedirect(reverse('payment_app:purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request, f'Your payment failed! Please try again')

    return render(request, 'payment_app/complete.html', {})

@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderID = tran_id
    order.ordered = True
    order.order_id = orderID
    order.payment_id = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('shop_app:home'))

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {'orders': orders}
    except:
        messages.warning(request, "You do not have an active order")
        return redirect('shop_app:home')
    
    return render(request, 'payment_app/order.html', context)