from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_view, name='items'),
    path('<int:pk>/', views.items_detail, name='item_detail'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('add_to_basket/<int:pk>/', views.add_to_basket, name='add_to_basket'),
]
