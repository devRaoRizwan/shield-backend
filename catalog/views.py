from django.http import Http404, HttpResponse
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inquiry, Product
from .permissions import IsStaffUser
from .serializers import (
    AdminLoginSerializer,
    InquiryAdminSerializer,
    InquiryCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductWriteSerializer,
)


class NumericSlugOrderingMixin:
    @staticmethod
    def _slug_sort_key(product):
        slug = (product.slug or "").strip()
        if slug.isdigit():
            return (0, int(slug), slug)
        return (1, slug)

    def get_sorted_products(self, queryset):
        return sorted(queryset, key=self._slug_sort_key)


class ProductListAPIView(NumericSlugOrderingMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.active()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.get_sorted_products(queryset), many=True)
        return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.active()


class ProductImageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        product = Product.objects.filter(slug=slug).first()
        if not product or not product.image_data:
            raise Http404("Image not found.")

        response = HttpResponse(product.image_data, content_type=product.image_content_type or "application/octet-stream")
        if product.image_name:
            response["Content-Disposition"] = f'inline; filename="{product.image_name}"'
        return response


class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff,
                },
            },
            status=status.HTTP_200_OK,
        )


class AdminProfileAPIView(APIView):
    permission_classes = [IsStaffUser]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
            }
        )


class AdminProductListCreateAPIView(NumericSlugOrderingMixin, generics.ListCreateAPIView):
    serializer_class = ProductWriteSerializer
    permission_classes = [IsStaffUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.get_sorted_products(queryset), many=True)
        return Response(serializer.data)


class AdminProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductWriteSerializer
    permission_classes = [IsStaffUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Product.objects.all()


class InquiryCreateAPIView(generics.CreateAPIView):
    serializer_class = InquiryCreateSerializer
    permission_classes = [AllowAny]


class AdminInquiryListAPIView(generics.ListAPIView):
    serializer_class = InquiryAdminSerializer
    permission_classes = [IsStaffUser]
    queryset = Inquiry.objects.all()


class AdminInquiryDetailAPIView(generics.DestroyAPIView):
    permission_classes = [IsStaffUser]
    queryset = Inquiry.objects.all()
