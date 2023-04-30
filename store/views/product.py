from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from ..serializers import CreateProductSerializer, ProductCommentSerializer
from ..models import Product, Comment
from ..utils import Actions, Filterer

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CreateProductSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_get(req):

    OPTIONS = ['products', 'categories', 'sub_categories']

    if req.method == "POST":
        data, status = Actions.create(serializer=CreateProductSerializer, data=req.data)
    
    if req.method == "GET":
        query = req.GET.get('query')
        selection = req.GET.get('selection')

        if selection != None:
            if selection not in OPTIONS:
                return Response({'message': 'Invalid search selection'}, 400)

        data, status = Actions.get(serializer=CreateProductSerializer, model=Product, 
                                   query=query, selection=selection, spy=Q)

    data = {
        "data": data
    }

    return Response(data, status)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single_product(serializer=CreateProductSerializer, model=Product, index=index, comments=Comment)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Product, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CreateProductSerializer, model=Product, index=index, data=req.data)

    data = {
        "data": data
    }
    
    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_comments(req, index):
    try:
        product = Product.objects.get(id=index)
    except Product.DoesNotExist:
        return Response(status=404)
    
    query = Comment.objects.filter(product=product.id)
    serializer = ProductCommentSerializer(query, many=True)

    data = {
        "data": serializer.data
    }

    return Response(data, 200)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def new_products(req):

    data, status = Filterer(model=Product, serializer=CreateProductSerializer, param='-date_added')

    data = {
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def trending_products(req):

    data, status = Filterer(model=Product, serializer=CreateProductSerializer, param='-views')

    data = {
        "data": data
    }

    return Response(data, status)