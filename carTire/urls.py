from django.contrib import admin
from django.urls import path, include
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", views.index, name="index"),
]

handler404 = "shop.views.redirect_to_index"
