from django.contrib import admin
from django.urls import path, re_path
from marketplace import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", views.health),
    path("v1/auth/register", views.register),
    path("v1/workspace", views.workspace),
    path("v1/workspace/<str:kind>", views.workspace),
    path("v1/workspace/<str:kind>/<uuid:pk>", views.workspace),
    path("v1/auctions/<uuid:pk>/events", views.auction_events),
    path("v1/file-upload/<uuid:pk>", views.file_upload),
    path("v1/file-download/<uuid:pk>", views.file_download),
    path("v1/export-download/<uuid:pk>", views.export_download),
    re_path(r"^v1/(?P<route>.*)$", views.contract_endpoint),
]
