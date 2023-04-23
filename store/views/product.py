from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CreateProductSerializer, ProductCommentSerializer
from ..models import Product, Comment

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CreateProductSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):
    if req.method == "POST":

        serializer = CreateProductSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    if req.method == "GET":
        query = Product.objects.all()
        serializer = CreateProductSerializer(query, many=True)
        
        return Response(serializer.data, 200)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=404)
    
    if req.method == 'GET':
        product_serializer = CreateProductSerializer(product, many=False)

        # increase views
        product.views += 1
        product.save()

        return Response(product_serializer.data)
    
    if req.method == 'DELETE':
        product.delete()
        return Response(status=204)
         
    if req.method == 'PUT':
        serializer = CreateProductSerializer(product, data=req.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        
        return Response(serializer.errors, status=400)
    
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