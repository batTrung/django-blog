from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('gioi-thieu/', views.about, name='about'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
