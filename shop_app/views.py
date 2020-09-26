from django.shortcuts import render, HttpResponseRedirect, HttpResponse

# Importing CBVs
from django.views.generic import ListView, DetailView

# Models
from .models import Product
# Create your views here.

class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'
    