from django.shortcuts import render, HttpResponseRedirect, HttpResponse

# Importing CBVs
from django.views.generic import ListView, DetailView

# Models
from .models import Product

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'

class ProductDetail(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'shop_app/product_detail.html'
    