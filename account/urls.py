from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	path('ajax/login/', views.login, name='login'),
	path('ajax/register/', views.register, name='register'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('<slug:username>/', views.profile, name='profile'),
]