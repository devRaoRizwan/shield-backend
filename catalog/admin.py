from django.contrib import admin

from .models import Inquiry, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_active",
        "sort_order",
        "updated_at",
    )
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "slug", "description", "details")
    ordering = ("sort_order", "name")
    list_editable = ("is_active", "sort_order")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Product Content",
            {
                "fields": (
                    "name",
                    "slug",
                    "image",
                    "description",
                    "details",
                    "customization_option",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": ("is_active", "sort_order"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    ordering = ("-created_at",)
    readonly_fields = ("full_name", "email", "subject", "message", "created_at")

    fieldsets = (
        (
            "Inquiry Details",
            {
                "fields": ("full_name", "email", "subject", "message"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )
