from django.contrib import admin
from django.urls import path

from otop_search_thailand import views

urlpatterns = [
    path('healthz', views.healthz, name='healthz'),
    path('', views.home, name='home'),
    path('products/', views.products_list, name='products'),
    path('provinces/', views.province_list, name='province_list'),
    path('provinces/<str:slug>/', views.province_detail, name='province_detail'),
    path('map/', views.map_view, name='map'),
    path('search/', views.search_view, name='search'),
    path('api/products.json', views.api_products_json, name='api_products_json'),
    path('api/products.geojson', views.api_products_geojson, name='api_products_geojson'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
]
