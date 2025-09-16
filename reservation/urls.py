from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add_to_bag/<int:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<int:item_id>/', views.adjust_bag, name='adjust_bag'),
    path(
        'remove/<int:item_id>/',
        views.remove_from_bag,
        name='remove_from_bag',
    ),
]
