from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt
from django.db.models import F, FloatField
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
    OpenApiExample,
)
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from locations.filters import PinCodeFilter, StateFilter, LocationFilter
from locations.models import PinCode, State, Location
from locations.serializers import PinCodeSerializer, StateSerializer, LocationSerializer


class PinCodeViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = PinCodeSerializer
    queryset = PinCode.objects.filter(is_active=True)
    filterset_class = PinCodeFilter

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


class StateViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.filter()
    filterset_class = StateFilter

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


# class LocationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
class LocationViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.filter()
    filterset_class = LocationFilter

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

    # @extend_schema(
    #     parameters=[
    #         OpenApiParameter(
    #             name="latitude", description="latitude", type=float, required=True
    #         ),
    #         OpenApiParameter(
    #             name="longitude", description="longitude", type=float, required=True
    #         ),
    #         OpenApiParameter(
    #             name="distance",
    #             description="distance in KM",
    #             type=float,
    #             required=False,
    #         ),
    #         OpenApiParameter(
    #             name="limit", description="limit", type=int, required=False
    #         ),
    #         OpenApiParameter(
    #             name="offset", description="offset", type=int, required=False
    #         ),
    #     ]
    # )
    # @action(detail=False, methods=["GET"])
    # def nearest(self, request, *args, **kwargs):
    #     params = self.request.query_params
    #     latitude = float(params.get("latitude"))
    #     longitude = float(params.get("longitude"))
    #     distance = float(params.get("distance", 5))
    #
    #     dlat = Radians(F("latitude") - latitude)
    #     dlong = Radians(F("longitude") - longitude)
    #
    #     a = Power(Sin(dlat / 2), 2) + Cos(Radians(latitude)) * Cos(
    #         Radians(F("latitude"))
    #     ) * Power(Sin(dlong / 2), 2)
    #
    #     sqrt1 = Sqrt(1 - a, output_field=FloatField())
    #
    #     c = 2 * ATan2(Sqrt(a), sqrt1, output_field=FloatField())
    #     d = 6371 * c
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     locations_near_me = (
    #         queryset.annotate(distance=d)
    #         .order_by("distance")
    #         .filter(distance__lte=distance)
    #     )
    #
    #     page = self.paginate_queryset(locations_near_me)
    #
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
