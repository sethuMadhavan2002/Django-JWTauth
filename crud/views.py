from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Product
from .serializers import ProductSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pysolr


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


@api_view(["GET"])
def searchView(request):
    query = request.GET.get("q", "")
    solr = pysolr.Solr(settings.SOLR_SERVER, always_commit=True)

    results = solr.search(query)
    # results = solr.search(q="title:Document")

    response_data = []

    for result in results:
        response_data.append(
            {
                "id": result["id"],
                "title": result.get("title", ""),
                "content": result.get("content", ""),
            }
        )

    return JsonResponse({"results": response_data})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pysolr
from django.conf import settings


@api_view(["POST"])
def addDocuments(request):
    try:
        if "documents" not in request.data:
            return Response(
                {"error": 'Missing "documents" key in request data'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        documents = request.data["documents"]
        if not isinstance(documents, list):
            return Response(
                {"error": '"documents" should be a list of documents'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        solr = pysolr.Solr(settings.SOLR_SERVER, always_commit=True)
        solr.add(documents)
        solr.commit()

        return Response(
            {"success": "Documents added successfully"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
