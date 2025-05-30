"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.conf.urls.static import static
from . import settings
from .settings import DEBUG
from .views import (
    login_redirects,
    index,
    testing_sbadmin2,
    healthcheck,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login_redirects/", login_redirects, name="login_redirects"),
    path("", index, name="index"),
    # ----------------------------------------------------------------
    # ----------------------------APP URLS----------------------------
    # ----------------------------------------------------------------
    path("accounts/v1/", include("accounts.urls"), name="accounts"),
    path("locations/v1/", include("locations.urls"), name="locations"),
    path("inventory/v1/", include("inventory.urls"), name="inventory"),
    path("rates/v1/", include("charges.urls"), name="rates"),
    path("healthcheck/", healthcheck, name="healthcheck"),
]

if DEBUG:
    urlpatterns += [
        path("testing_sbadmin2/", testing_sbadmin2, name="dashboard"),
        path("api/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
