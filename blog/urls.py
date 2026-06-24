from django.urls import path, include
from blog import admin, views

app_name = 'blog'

urlpatterns = [
    path('posts/create/', views.post_create, name = "post_create"),
    path('posts/<int:pk>', views.post_detail, name = "post_detail"),
    path('post/', views.post_list, name='post_list'),

    path('users/<int:user_id>/posts/', views.user_posts, name="user_posts"),
    path('posts/<int:pk>/edite/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete')
]