from django.contrib import admin
from .models import Province, Product


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","province","category","rating","phone","latitude","longitude")
    list_filter = ("province","category")
    search_fields = ("name","province__name","phone","address")
