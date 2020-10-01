from django.urls import path
from . import views

app_name = 'payment_app'

urlpatterns = [
    path('checkout/', views.check_out, name='checkout'),
    path('pay/', views.payment, name='payment'),
    path('status/', views.complete, name='complete'),
]