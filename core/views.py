import datetime

import pytz
from django.shortcuts import render, redirect
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from main.constants import IST
from main.serializers import StatusSerializer


def login_redirects(request):
    if request.user.is_authenticated:
        # TODO: TEMPLATE LOGIN REDIRECTS GO HERE
        return redirect("dashboard")
    return redirect("login")


def index(request):
    return render(request, template_name="index.html")


# ----------------------------------------------------------------
# ----------------------------TEST URLS---------------------------
# ----------------------------------------------------------------
def testing_sbadmin2(request):
    return render(request, template_name="testing/testing_sbadmin2.html")


@extend_schema(
    description="System health check",
    responses={200: StatusSerializer},
    examples=[
        OpenApiExample(
            "1",
            summary="Successful Health",
            value={
                "status": "ok",
                "system_time": str(datetime.datetime.now()),
            },
            request_only=False,
            response_only=True,
        )
    ],
)
@api_view(["GET"])
def healthcheck(request):
    return Response(
        StatusSerializer(
            {"status": "ok", "system_time": str(datetime.datetime.now(tz=IST))}
        ).data,
        status=status.HTTP_200_OK,
    )
