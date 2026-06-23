from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
   path('register/', views.register_view, name='register'),
   path('login/', views.login_view, name='login'),
   path('account/', views.account_view, name='account'),
   path('logout/', views.logout_view, name='logout')
]