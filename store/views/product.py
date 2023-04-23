from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CreateProductSerializer, ProductCommentSerializer
from ..models import Product, Comment
from ..utils import Actions

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CreateProductSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        data, status = Actions.create(serializer=CreateProductSerializer, data=req.data)
    
    if req.method == "GET":
        data, status = Actions.get(serializer=CreateProductSerializer, model=Product)

    return Response(data, status)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=CreateProductSerializer, model=Product, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Product, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CreateProductSerializer, model=Product, index=index, data=req.data)
    
    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(req, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=404)
    
    query = Comment.objects.filter(product=id)
    serializer = ProductCommentSerializer(query, many=True)

    return Response(serializer.data, 200)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_products(req):

    ...