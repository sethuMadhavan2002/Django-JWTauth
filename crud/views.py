from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def ProductViewSet(request):
    objects_from_replica = Product.get_objects_from_replica()
    serializer = ProductSerializers(objects_from_replica, many=True)
    return JsonResponse({"message": "Read Using Replica Set", "data": serializer.data})


@api_view(["GET"])
def ProductViewByID(request, id):
    objects_from_replica = Product.objects.using("read_replica").filter(id=id)
    serializer = ProductSerializers(objects_from_replica, many=True)
    return JsonResponse({"message": "Read Using Replica Set", "data": serializer.data})


@api_view(["POST"])
def AddProductData(request):
    data = request.data
    queryset = Product(name=data["name"], price=data["price"])
    queryset.save_to_master()
    return JsonResponse({"message": "Write Using Master Set"}, safe=False)


@api_view(["PUT"])
def UpdateProduct(request, id):
    data = request.data
    instance = Product.objects.get(id=id)
    instance.name = data["name"]
    instance.price = data["price"]
    instance.save_to_master()
    print(instance)
    serializer = ProductSerializers(instance)
    return JsonResponse(
        {"message": "Write Using Master Set", "data": serializer.data}, safe=False
    )


@api_view(["DELETE"])
def DeleteProduct(request, id):
    instance = Product.objects.get(id=id)
    instance.delete()
    return JsonResponse({"message": "product deleted"})
