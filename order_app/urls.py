from django.urls import path
from . import views

app_name = 'order_app'

urlpatterns = [
    path('add/<pk>/', views.add_to_cart, name='add'),

]