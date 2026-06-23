from django.urls import path, include
from blog import admin, views

app_name = 'blog'

urlpatterns = [
    path('posts/create/', views.post_create, name = "post_create"),
    path('posts/<int:pk>', views.post_detail, name = "post_detail"),
    path('post/', views.post_list, name='post_list')
]