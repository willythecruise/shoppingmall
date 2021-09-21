from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
 path('search/', views.product_search, name='product_search'),
 path('', views.product_list, name='product_list'),
 path('<slug:category_slug>/', views.product_list,
 name='product_list_by_category'),
 path('<int:id>/<slug:slug>/', views.product_detail,
 name='product_detail'),
]
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,
     document_root=settings.MEDIA_ROOT)
