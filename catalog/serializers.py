from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Inquiry, Product


class ProductBaseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "image",
            "description",
            "details",
            "customization_option",
        )


class ProductListSerializer(ProductBaseSerializer):
    class Meta(ProductBaseSerializer.Meta):
        fields = (
            "name",
            "slug",
            "image",
            "description",
            "customization_option",
        )


class ProductDetailSerializer(ProductBaseSerializer):
    pass


class ProductWriteSerializer(ProductBaseSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = (
            "id",
            "name",
            "slug",
            "image",
            "description",
            "details",
            "customization_option",
            "is_active",
            "sort_order",
        )


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        user = authenticate(
            request=request,
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_staff:
            raise serializers.ValidationError("This account does not have admin access.")

        attrs["user"] = user
        return attrs


class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("id", "full_name", "email", "subject", "message", "created_at")
        read_only_fields = ("id", "created_at")


class InquiryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("id", "full_name", "email", "subject", "message", "created_at")
