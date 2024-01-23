from rest_framework import serializers
from haystack.query import SearchQuerySet
from .models import Product, Document


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
