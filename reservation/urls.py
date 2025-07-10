from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='reservation'),
    path('add/<int:item_id>/', views.add_to_bag, name='add_reservation'),
    path('adjust/<int:item_id>/', views.adjust_bag, name='adjust_reservation'),
    path('remove/<int:item_id>/', views.remove_from_bag, name='remove_reservation'),
]
