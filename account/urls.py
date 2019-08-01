from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
	path('login/', views.login, name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('register/', views.register, name='register'),
	path('proflie/edit/', views.edit_profile, name='edit_profile'),
	path('photo/update/', views.photo_update, name='photo_update'),
]