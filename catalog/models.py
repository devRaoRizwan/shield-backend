import mimetypes
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)
    image_name = models.CharField(max_length=255, blank=True)
    image_content_type = models.CharField(max_length=100, blank=True)
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

    def store_uploaded_image(self, uploaded_image, name=None, content_type=None):
        if not uploaded_image:
            return

        if hasattr(uploaded_image, "seek"):
            uploaded_image.seek(0)

        self.image_data = uploaded_image.read()
        self.image_name = Path(name or getattr(uploaded_image, "name", "product-image")).name
        self.image_content_type = (
            content_type
            or getattr(uploaded_image, "content_type", "")
            or mimetypes.guess_type(self.image_name)[0]
            or "application/octet-stream"
        )
        self.image = None

    def get_image_url(self, request=None):
        if self.image_data:
            url = reverse("catalog:product-image", kwargs={"slug": self.slug})
            return request.build_absolute_uri(url) if request else url

        if self.image:
            url = self.image.url
            return request.build_absolute_uri(url) if request else url

        return ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.image and getattr(self.image, "_committed", True) is False:
            self.store_uploaded_image(
                self.image.file,
                name=self.image.name,
                content_type=getattr(self.image.file, "content_type", None),
            )

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
