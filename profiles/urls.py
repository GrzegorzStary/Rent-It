from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('my-profile/', views.profile_view, name='user_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('listed-items/', views.listed_items, name='listed_items'),
    path("rented_items/", views.rented_items, name='rented_items'),
]
