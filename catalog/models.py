from django.db import models
from django.utils.text import slugify


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="products/")
    description = models.TextField()
    details = models.TextField()
    customization_option = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ("sort_order", "name")
        indexes = [
            models.Index(fields=("is_active", "sort_order")),
            models.Index(fields=("slug",)),
        ]
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Inquiry(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("created_at",)),
            models.Index(fields=("email",)),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
