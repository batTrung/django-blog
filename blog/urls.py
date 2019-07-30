from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('gioi-thieu/', views.about, name='about'),
]
