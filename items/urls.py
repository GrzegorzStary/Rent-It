from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_view, name='items'),
    path('<int:pk>/', views.items_detail, name='item_detail'),
]
