from django.contrib import admin
from django.urls import path, include
from .views import (
    ProductViewSet,
    AddProductData,
    UpdateProduct,
    DeleteProduct,
    ProductViewByID,
)


urlpatterns = [
    path("get/", ProductViewSet, name="get"),
    path("get-by-id/<int:id>", ProductViewByID, name="get_by_id"),
    path("add/", AddProductData, name="add"),
    path("update/<int:id>", UpdateProduct, name="update"),
    path("delete/<int:id>", DeleteProduct, name="delete"),
]
