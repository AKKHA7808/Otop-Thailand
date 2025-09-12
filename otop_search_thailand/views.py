from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.db.models import Count
from django.conf import settings
from functools import lru_cache
import os

from .models import Province, Product

# ---------- Home / About ----------
def home(request):
    total_products = Product.objects.count()
    total_provinces = Province.objects.count()
    top_categories = (
        Product.objects.values('category')
        .exclude(category="")
        .annotate(c=Count('id'))
        .order_by('-c')[:8]
    )
    top_provinces = (
        Province.objects.annotate(product_total=Count('products'))
        .order_by('-product_total','name')[:8]
    )
    top_products = Product.objects.order_by('-rating','name')[:8]
    return render(request, "home.html", {
        "total_products": total_products,
        "total_provinces": total_provinces,
        "top_categories": top_categories,
        "top_provinces": top_provinces,
        "top_products": top_products,
    })

def about(request):
    return render(request, "about.html")

# ---------- Products / Provinces ----------
def products_list(request):
    qs = Product.objects.select_related("province").order_by("name")
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            models.Q(name__icontains=q) |
            models.Q(province__name__icontains=q) |
            models.Q(category__icontains=q) |
            models.Q(description__icontains=q)
        )
    return render(request, "products_list.html", {"products": qs, "q": q})

def province_list(request):
    provinces = Province.objects.annotate(product_total=Count("products")).order_by("name")
    return render(request, "provinces.html", {"provinces": provinces})

def province_detail(request, slug):
    province = get_object_or_404(Province, slug=slug)
    products = Product.objects.filter(province=province).order_by("-rating", "name")
    return render(request, "province_detail.html", {"province": province, "products": products})

# ---------- Search + Map ----------
def search_view(request):
    return render(request, "search.html")

def map_view(request):
    return render(request, 'map.html', {
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    })

# ---------- APIs ----------
def api_products_json(request):
    data = [{
        "name": p.name,
        "province": p.province.name,
        "category": p.category,
        "rating": float(p.rating or 0),
        "address": p.address,
        "phone": p.phone,
        "lat": float(p.latitude) if p.latitude is not None else None,
        "lng": float(p.longitude) if p.longitude is not None else None,
        "description": p.description,
        "image_url": p.image_url,
    } for p in Product.objects.select_related("province").all()]
    return JsonResponse(data, safe=False)


def api_products_geojson(request):
    feats = []
    for p in Product.objects.select_related("province").all():
        if p.latitude is None or p.longitude is None:
            continue
        feats.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [float(p.longitude), float(p.latitude)]},
            "properties": {
                "name": p.name,
                "province": p.province.name,
                "category": p.category,
                "rating": float(p.rating or 0),
                "image_url": p.image_url,
                "address": p.address,
                "phone": p.phone,
            }
        })
    return JsonResponse({"type": "FeatureCollection", "features": feats})


@lru_cache(maxsize=1)
def _cached_file_bytes(mtime):
    with open(settings.OTOP_JSON_PATH, 'rb') as f:
        return f.read()

def api_file_json(request):
    path = getattr(settings, 'OTOP_JSON_PATH', None)
    if not path or not os.path.exists(path):
        return JsonResponse({"error": "OTOP_JSON_PATH not configured or file not found"}, status=404)
    mtime = os.path.getmtime(path)
    return HttpResponse(_cached_file_bytes(mtime), content_type='application/json; charset=utf-8')
