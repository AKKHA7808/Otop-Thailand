from django.db import models
from django.utils.text import slugify


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def _generate_unique_slug(self, base):
        slug = slugify(base, allow_unicode=True)
        original = slug
        suffix = 1
        while Province.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{original}-{suffix}"
            suffix += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name="products")
    category = models.CharField(max_length=120, blank=True, default="")

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, default="")
    image_url = models.URLField(max_length=500, null=True, blank=True)

    address = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=120, blank=True, default="")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["province", "category"]),
            models.Index(fields=["latitude", "longitude"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name", "province"], name="uniq_product_in_province"),
        ]

    def __str__(self):
        return self.name
