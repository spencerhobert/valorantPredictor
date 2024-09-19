from django.urls import path
from . import views

urlpatterns = [
    path('fit/', views.fit, name='fit'),
    path('predict/', views.predict, name='predict')
]