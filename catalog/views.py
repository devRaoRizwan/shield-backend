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


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.active()


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.active()


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


class AdminProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductWriteSerializer
    permission_classes = [IsStaffUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Product.objects.all().order_by("sort_order", "name")


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
