from django.urls import path

from .views import (
    AdminInquiryDetailAPIView,
    AdminInquiryListAPIView,
    AdminLoginAPIView,
    AdminProductDetailAPIView,
    AdminProductListCreateAPIView,
    AdminProfileAPIView,
    InquiryCreateAPIView,
    ProductDetailAPIView,
    ProductListAPIView,
)

app_name = "catalog"

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("inquiries/", InquiryCreateAPIView.as_view(), name="inquiry-create"),
    path("admin/auth/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("admin/auth/me/", AdminProfileAPIView.as_view(), name="admin-profile"),
    path("admin/inquiries/", AdminInquiryListAPIView.as_view(), name="admin-inquiry-list"),
    path("admin/inquiries/<int:pk>/", AdminInquiryDetailAPIView.as_view(), name="admin-inquiry-detail"),
    path("admin/products/", AdminProductListCreateAPIView.as_view(), name="admin-product-list"),
    path("admin/products/<int:pk>/", AdminProductDetailAPIView.as_view(), name="admin-product-detail"),
]
