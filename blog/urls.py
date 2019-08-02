from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('gioi-thieu/', views.about, name='about'),
    path('post/search/', views.post_search, name='post_search'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('ajax/update/like/', views.update_like, name='update_like'),
    path('ajax/post/<slug:slug>/comment/', views.comment_create, name='comment_create'),
    path('ajax/comment/<int:id>/reply/', views.comment_reply, name='comment_reply'),
    path('ajax/comment/update/like/', views.update_comment_like, name='update_comment_like'),
]
