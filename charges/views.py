from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiExample
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from charges.filters import OfferFilter, ParkingSpotRateFilter, PaymentModeFilter
from charges.models import Offer, ParkingSpotRate, PaymentMode
from charges.serializers import (
    OfferSerializer,
    ParkingSpotRateSerializer,
    PaymentModeSerializer,
    ParkingSpotRateCompleteSerializer,
)


class OfferViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.filter(is_active=True)
    filterset_class = OfferFilter

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.first(), many=False).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.filter()[:1], many=True).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ParkingSpotRateViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = ParkingSpotRateCompleteSerializer
    queryset = ParkingSpotRate.objects.filter(is_active=True)
    filterset_class = ParkingSpotRateFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="floor", description="Floor", type=int, required=True
            ),
        ],
        responses={200: ParkingSpotRateCompleteSerializer},
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.first(), many=False).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ParkingSpotRateCompleteSerializer(instance)
        return Response(serializer.data)

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.filter()[:1], many=True).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PaymentModeViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = PaymentModeSerializer
    queryset = PaymentMode.objects.filter(is_active=True)
    filterset_class = PaymentModeFilter

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.first(), many=False).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(queryset.filter()[:1], many=True).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
