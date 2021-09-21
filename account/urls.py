from django.urls import path,include,reverse
from django.contrib.auth import views as auth_views
from . import views
app_name= 'account'

urlpatterns=[
path('edit/', views.edit, name='edit'),
path('dashboard/', views.dashboard, name='dashboard'),
path('', include('django.contrib.auth.urls')),
path('register/', views.register, name='register'),
# reset password urls
 ]
