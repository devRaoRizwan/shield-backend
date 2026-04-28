from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from .models import Inquiry, Product


TEST_IMAGE_BYTES = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
    b"\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00"
    b"\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02"
    b"\x44\x01\x00\x3b"
)


@override_settings(MEDIA_ROOT="test_media")
class ProductAPITests(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(
            "product.gif",
            TEST_IMAGE_BYTES,
            content_type="image/gif",
        )
        self.product = Product.objects.create(
            name="Shield Backpack",
            slug="shield-backpack",
            image=image,
            description="A featured product",
            details="Full product details for the frontend detail page.",
            customization_option="Custom patch available",
            is_active=True,
            sort_order=1,
        )
        Product.objects.create(
            name="Hidden Product",
            slug="hidden-product",
            image=SimpleUploadedFile(
                "hidden.gif",
                TEST_IMAGE_BYTES,
                content_type="image/gif",
            ),
            description="Should not appear publicly",
            details="Inactive product",
            customization_option="None",
            is_active=False,
            sort_order=99,
        )

    def test_product_list_returns_only_active_products(self):
        response = self.client.get(reverse("catalog:product-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["slug"], self.product.slug)

    def test_product_detail_uses_slug_lookup(self):
        response = self.client.get(
            reverse("catalog:product-detail", kwargs={"slug": self.product.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slug"], self.product.slug)
        self.assertIn("/media/products/", response.json()["image"])

    def test_product_detail_returns_404_for_invalid_slug(self):
        response = self.client.get(
            reverse("catalog:product-detail", kwargs={"slug": "missing-product"})
        )

        self.assertEqual(response.status_code, 404)


@override_settings(MEDIA_ROOT="test_media")
class AdminProductAPITests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.staff_user = self.user_model.objects.create_user(
            username="admin",
            password="strong-pass-123",
            is_staff=True,
        )
        self.non_staff_user = self.user_model.objects.create_user(
            username="member",
            password="member-pass-123",
            is_staff=False,
        )
        self.token = Token.objects.create(user=self.staff_user)
        self.non_staff_token = Token.objects.create(user=self.non_staff_user)
        self.product = Product.objects.create(
            name="Admin Shield",
            slug="admin-shield",
            image=SimpleUploadedFile(
                "admin.gif",
                TEST_IMAGE_BYTES,
                content_type="image/gif",
            ),
            description="Admin managed product",
            details="Editable details",
            customization_option="Gold trim",
            is_active=True,
            sort_order=1,
        )

    def auth_headers(self):
        return {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

    def non_staff_auth_headers(self):
        return {"HTTP_AUTHORIZATION": f"Token {self.non_staff_token.key}"}

    def test_admin_login_returns_token_for_staff_user(self):
        response = self.client.post(
            reverse("catalog:admin-login"),
            {"username": "admin", "password": "strong-pass-123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertEqual(response.json()["user"]["username"], "admin")

    def test_admin_products_require_authentication(self):
        response = self.client.get(reverse("catalog:admin-product-list"))
        self.assertEqual(response.status_code, 401)

    def test_admin_can_create_product(self):
        response = self.client.post(
            reverse("catalog:admin-product-list"),
            {
                "name": "Fresh Product",
                "slug": "fresh-product",
                "image": SimpleUploadedFile(
                    "fresh.gif",
                    TEST_IMAGE_BYTES,
                    content_type="image/gif",
                ),
                "description": "Created from API",
                "details": "Full details",
                "customization_option": "Silver plate",
                "is_active": True,
                "sort_order": 2,
            },
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(slug="fresh-product").exists())

    def test_admin_can_update_product(self):
        response = self.client.patch(
            reverse("catalog:admin-product-detail", kwargs={"pk": self.product.pk}),
            {"name": "Updated Admin Shield", "sort_order": 5},
            content_type="application/json",
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Admin Shield")
        self.assertEqual(self.product.sort_order, 5)

    def test_admin_can_delete_product(self):
        response = self.client.delete(
            reverse("catalog:admin-product-detail", kwargs={"pk": self.product.pk}),
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_public_can_create_inquiry(self):
        response = self.client.post(
            reverse("catalog:inquiry-create"),
            {
                "full_name": "Muhammad Aneeq",
                "email": "aneeq@example.com",
                "subject": "Need a custom shield",
                "message": "Please contact me about pricing and design options.",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Inquiry.objects.filter(email="aneeq@example.com").exists())

    def test_admin_can_list_inquiries(self):
        Inquiry.objects.create(
            full_name="Test User",
            email="test@example.com",
            subject="Test Inquiry",
            message="I would like more information.",
        )

        response = self.client.get(
            reverse("catalog:admin-inquiry-list"),
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["email"], "test@example.com")

    def test_admin_can_delete_inquiry(self):
        inquiry = Inquiry.objects.create(
            full_name="Delete Me",
            email="delete@example.com",
            subject="Remove Inquiry",
            message="Please remove this from admin inbox.",
        )

        response = self.client.delete(
            reverse("catalog:admin-inquiry-detail", kwargs={"pk": inquiry.pk}),
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Inquiry.objects.filter(pk=inquiry.pk).exists())

    def test_admin_delete_inquiry_returns_404_when_not_found(self):
        response = self.client.delete(
            reverse("catalog:admin-inquiry-detail", kwargs={"pk": 999999}),
            **self.auth_headers(),
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_delete_inquiry_requires_authentication(self):
        inquiry = Inquiry.objects.create(
            full_name="Protected Inquiry",
            email="protected@example.com",
            subject="Protected",
            message="Should require auth.",
        )

        response = self.client.delete(
            reverse("catalog:admin-inquiry-detail", kwargs={"pk": inquiry.pk}),
        )

        self.assertEqual(response.status_code, 401)

    def test_admin_delete_inquiry_forbids_non_staff_users(self):
        inquiry = Inquiry.objects.create(
            full_name="Staff Only",
            email="staffonly@example.com",
            subject="Forbidden",
            message="Non-staff should not delete this.",
        )

        response = self.client.delete(
            reverse("catalog:admin-inquiry-detail", kwargs={"pk": inquiry.pk}),
            **self.non_staff_auth_headers(),
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Inquiry.objects.filter(pk=inquiry.pk).exists())
