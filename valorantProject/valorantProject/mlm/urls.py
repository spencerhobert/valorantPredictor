from django.urls import path
from . import views

urlpatterns = [
    path('mlm/', views.mlm, name='mlm')
]