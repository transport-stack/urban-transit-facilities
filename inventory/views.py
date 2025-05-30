from django.db import transaction
from django.db.models import F, FloatField
from django.db.models.functions import Radians, Sin, Power, Cos, Sqrt, ATan2
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from accounts.constants import UserType
from accounts.models import MyUser
from inventory.filters import (
    FloorPlanFilter,
    ParkingSpotFilter,
    VehicleTypeFilter,
    FloorPlanPredictionFilter,
)
from inventory.models import (
    FloorPlan,
    ParkingSpot,
    VehicleType,
    ParkingSpotAvailability,
    FloorPlanPrediction,
)
from inventory.serializers import (
    FloorPlanSerializer,
    ParkingSpotSerializer,
    VehicleTypeSerializer,
    ParkingSpotAvailabilitySerializer,
    FloorPlanPredictionSerializer,
)
from locations.models import Location
from datetime import datetime, time
from pytz import timezone

from main.constants import IST
from main.serializers import StatusSerializer


class FloorPlanViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = FloorPlanSerializer
    queryset = FloorPlan.objects.filter(is_active=True)
    filterset_class = FloorPlanFilter

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                # value=serializer_class(queryset.first(), many=False).data,
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
                # value=serializer_class(queryset.filter()[:1], many=True).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="location", description="Location PK", type=int, required=True
            ),
        ],
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                # value=serializer_class(queryset.filter()[:1], many=True).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    @action(detail=False, methods=["GET"], url_path="of-location")
    def of_location(self, request, *args, **kwargs):
        params = self.request.query_params
        location = params.get("location")
        if not location:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            location = int(location)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        location = get_object_or_404(Location, pk=location)
        return Response(self.get_serializer(location.location_floors, many=True).data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude", description="latitude", type=float, required=True
            ),
            OpenApiParameter(
                name="longitude", description="longitude", type=float, required=True
            ),
            OpenApiParameter(
                name="distance",
                description="distance in KM",
                type=float,
                required=False,
            ),
            OpenApiParameter(
                name="limit", description="limit", type=int, required=False
            ),
            OpenApiParameter(
                name="offset", description="offset", type=int, required=False
            ),
            OpenApiParameter(
                name="location", description="location", type=str, required=False
            ),
            OpenApiParameter(
                name="address", description="address", type=str, required=False
            ),
            OpenApiParameter(
                name="vehicle_type",
                description="Vehicle Type",
                type=str,
                required=False,
            ),
        ],
    )
    @action(detail=False, methods=["GET"])
    def nearest(self, request, *args, **kwargs):
        params = self.request.query_params
        latitude = float(params.get("latitude"))
        longitude = float(params.get("longitude"))
        distance = float(params.get("distance", 5))

        dlat = Radians(F("location__latitude") - latitude)
        dlong = Radians(F("location__longitude") - longitude)

        a = Power(Sin(dlat / 2), 2) + Cos(Radians(latitude)) * Cos(
            Radians(F("location__latitude"))
        ) * Power(Sin(dlong / 2), 2)

        sqrt1 = Sqrt(1 - a, output_field=FloatField())

        c = 2 * ATan2(Sqrt(a), sqrt1, output_field=FloatField())
        d = 6371 * c

        queryset = self.filter_queryset(self.get_queryset())

        locations_near_me = (
            queryset.annotate(distance=d)
            .order_by("distance")
            .filter(distance__lt=distance)
        )

        page = self.paginate_queryset(locations_near_me)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude", description="latitude", type=float, required=True
            ),
            OpenApiParameter(
                name="longitude", description="longitude", type=float, required=True
            ),
            OpenApiParameter(
                name="distance",
                description="distance in KM",
                type=float,
                required=False,
            ),
            OpenApiParameter(
                name="limit", description="limit", type=int, required=False
            ),
            OpenApiParameter(
                name="offset", description="offset", type=int, required=False
            ),
            OpenApiParameter(
                name="location", description="location", type=str, required=False
            ),
            OpenApiParameter(
                name="address", description="address", type=str, required=False
            ),
            OpenApiParameter(
                name="vehicle_type",
                description="Vehicle Type",
                type=str,
                required=False,
            ),
        ],
    )
    @action(detail=False, methods=["GET"])
    def nearest_v2(self, request, *args, **kwargs):
        params = self.request.query_params
        latitude = float(params.get("latitude"))
        longitude = float(params.get("longitude"))
        distance = float(params.get("distance", 5))

        dlat = Radians(F("latitude") - latitude)
        dlong = Radians(F("longitude") - longitude)

        a = Power(Sin(dlat / 2), 2) + Cos(Radians(latitude)) * Cos(
            Radians(F("latitude"))
        ) * Power(Sin(dlong / 2), 2)

        sqrt1 = Sqrt(1 - a, output_field=FloatField())

        c = 2 * ATan2(Sqrt(a), sqrt1, output_field=FloatField())
        d = 6371 * c

        queryset = self.filter_queryset(self.get_queryset())

        locations_near_me = (
            queryset.annotate(distance=d)
            .order_by("distance")
            .filter(distance__lt=distance)
        )

        page = self.paginate_queryset(locations_near_me)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ParkingSpotAvailabilitySerializer,
        responses={200: StatusSerializer(many=False)},
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=StatusSerializer(
                    {
                        "status": "ok",
                        "system_time": str(datetime.now()),
                    }
                ).data,
                request_only=False,
                response_only=True,
            )
        ],
    )
    @action(detail=True, methods=["POST"])
    def availability(self, request, *args, **kwargs):
        floor = self.get_object()
        user = self.request.user
        if user.is_anonymous or user.type != UserType.SERVICE_PROVIDER:
            return Response(
                StatusSerializer(
                    {
                        "status": "You are not allowed to access this endpoint.",
                        "system_time": str(datetime.now(tz=IST)),
                    }
                ).data,
                status.HTTP_401_UNAUTHORIZED,
            )
        if (
            user.service_provider is None
            or floor.location.provider is None
            or floor.location.provider.pk != user.service_provider.pk
        ):
            return Response(
                StatusSerializer(
                    {
                        "status": "You are not allowed to access this endpoint.",
                        "system_time": str(datetime.now(tz=IST)),
                    }
                ).data,
                status.HTTP_403_FORBIDDEN,
            )
        serializer = ParkingSpotAvailabilitySerializer(data=self.request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                spot, _ = ParkingSpotAvailability.objects.get_or_create(
                    floor=floor, vehicle_type=serializer.validated_data["vehicle_type"]
                )
                for attr, value in serializer.validated_data.items():
                    setattr(spot, attr, value)
                spot.added_by = user
                spot.save()
        except Exception as e:
            return Response(
                StatusSerializer(
                    {"status": str(e), "system_time": str(datetime.now(tz=IST))}
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            StatusSerializer(
                {"status": "ok", "system_time": str(datetime.now(tz=IST))}
            ).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=ParkingSpotAvailabilitySerializer(many=True),
        responses={200: StatusSerializer(many=False)},
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=StatusSerializer(
                    {
                        "status": "ok",
                        "system_time": str(datetime.now()),
                    }
                ).data,
                request_only=False,
                response_only=True,
            )
        ],
    )
    @action(detail=True, methods=["POST"])
    @transaction.atomic
    def availabilities(self, request, *args, **kwargs):
        floor = self.get_object()
        user = self.request.user
        if user.is_anonymous or user.type != UserType.SERVICE_PROVIDER:
            return Response(
                StatusSerializer(
                    {
                        "status": "You are not allowed to access this endpoint.",
                        "system_time": str(datetime.now(tz=IST)),
                    }
                ).data,
                status.HTTP_401_UNAUTHORIZED,
            )
        if (
            user.service_provider is None
            or floor.location.provider is None
            or floor.location.provider.pk != user.service_provider.pk
        ):
            return Response(
                StatusSerializer(
                    {
                        "status": "You are not allowed to access this endpoint.",
                        "system_time": str(datetime.now(tz=IST)),
                    }
                ).data,
                status.HTTP_403_FORBIDDEN,
            )
        serializer = ParkingSpotAvailabilitySerializer(
            data=self.request.data, many=True
        )
        try:
            if serializer.is_valid(raise_exception=True):
                for data_obj in serializer.validated_data:
                    spot, _ = ParkingSpotAvailability.objects.get_or_create(
                        floor=floor, vehicle_type=data_obj["vehicle_type"]
                    )
                    for attr, value in data_obj.items():
                        setattr(spot, attr, value)
                    spot.added_by = user
                    spot.save()
        except Exception as e:
            return Response(
                StatusSerializer(
                    {"status": str(e), "system_time": str(datetime.now(tz=IST))}
                ).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            StatusSerializer(
                {"status": "ok", "system_time": str(datetime.now(tz=IST))}
            ).data,
            status=status.HTTP_200_OK,
        )


class VehicleTypeViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = VehicleTypeSerializer
    queryset = VehicleType.objects.filter(is_active=True)
    filterset_class = VehicleTypeFilter

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


class ParkingSpotViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    serializer_class = ParkingSpotSerializer
    queryset = ParkingSpot.objects.filter(is_active=True)
    filterset_class = ParkingSpotFilter

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


class FloorPlanPredictionViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    # queryset = FloorPlanPrediction.objects.filter(is_active=True)
    serializer_class = FloorPlanPredictionSerializer
    filterset_class = FloorPlanPredictionFilter

    @extend_schema(
        examples=[
            OpenApiExample(
                "1",
                summary="Success",
                value=serializer_class(
                    FloorPlanPrediction.objects.first(), many=False
                ).data,
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
                value=serializer_class(
                    FloorPlanPrediction.objects.filter()[:1], many=True
                ).data,
                request_only=False,
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        ist = timezone("Asia/Kolkata")
        current_time_ist = datetime.now(ist)
        current_hour = time(current_time_ist.hour, 0)
        current_day_name = current_time_ist.strftime("%A")

        return FloorPlanPrediction.objects.filter(
            is_active=True, time=current_hour, day__day=current_day_name
        )
