from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from ..serializers import CreateProductSerializer, ProductCommentSerializer
from ..models import Product, Comment
from ..utils import Actions, Filterer, ReadOnly

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CreateProductSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser|ReadOnly])
def create_get(req):

    OPTIONS = ['products']

    if req.method == "POST":
        data, status = Actions.create(serializer=CreateProductSerializer, data=req.data)
    
    if req.method == "GET":
        query = req.GET.get('query')
        selection = req.GET.get('selection')

        if selection != None:
            if selection not in OPTIONS:
                data = {
                    "status": 400,
                    "message": "Invalid search selection"
                }
                return Response(data, 400)

        data, status = Actions.get(serializer=CreateProductSerializer, model=Product, 
                                   query=query, selection=selection, spy=Q, req=req)
        
        for i in data["results"]:
            i["product_img"] = f'http://hairshine.pythonanywhere.com{i["product_img"]}'
        

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser|ReadOnly])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single_product(serializer=CreateProductSerializer, model=Product, index=index, comments=Comment)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Product, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CreateProductSerializer, model=Product, index=index, data=req.data)

    data = {
        "status": status,
        "data": data
    }
    
    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([ReadOnly])
def get_comments(req, index):
    try:
        product = Product.objects.get(id=index)
    except Product.DoesNotExist:
        data = {
            "status": 404,
            "message": "This product does not exist"
        }
        return Response(data, 404)
    
    query = Comment.objects.filter(product=product.id)
    serializer = ProductCommentSerializer(query, many=True)

    data = {
        "status": 200,
        "data": serializer.data
    }

    return Response(data, 200)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([ReadOnly])
def new_products(req):

    data, status = Filterer(model=Product, serializer=CreateProductSerializer, 
                            param='-date_added', req=req)
    
    for i in data["results"]:
        i["product_img"] = f'http://hairshine.pythonanywhere.com{i["product_img"]}'

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([ReadOnly])
def trending_products(req):

    data, status = Filterer(model=Product, serializer=CreateProductSerializer, 
                            param='-views', req=req)
    
    for i in data["results"]:
        i["product_img"] = f'http://hairshine.pythonanywhere.com{i["product_img"]}'

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)