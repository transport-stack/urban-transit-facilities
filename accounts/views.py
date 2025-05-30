import uuid

from django.contrib import messages
from django.shortcuts import render, redirect
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import MyUser
from accounts.permissions import IsUserOwner
from accounts.serializers import MyUserSerializer
from core.mixins import ViewSetPermissionByMethodMixin
from django.contrib.auth import logout


class MyUserViewSet(ViewSetPermissionByMethodMixin, GenericViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.filter(is_superuser=False, is_active=True).all()
    permission_classes = [IsAuthenticated]
    permission_action_classes = dict(
        create=(AllowAny,),
        retrieve=(IsUserOwner,),
        update=(IsUserOwner,),
        partial_update=(IsUserOwner,),
        login=(AllowAny,),
    )

    @extend_schema(
        description="Get User Details",
        responses={
            200: OpenApiResponse(
                description="Successfully fetched.", response=serializer_class
            )
        },
    )
    @action(detail=False, methods=["GET"])
    def my(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def LogoutView(request):
    logout(request)
    return redirect("login_redirects")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = MyUser.objects.get(username=username)
            # TODO: TEMPLATE FORGOT PASS FLOW
        except MyUser.DoesNotExist:
            pass
        messages.add_message(
            request,
            messages.SUCCESS,
            "We have contacted you with further actions!",
        )
        return redirect("login")
    return render(request, "registration/forgot_password.html")
