from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import PostSubCategorySerializer, GetSubCategorySerializer, SubProductSerializer
from ..models import SubCategory, Product

@swagger_auto_schema(methods=['post', 'get'], request_body=PostSubCategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        
        serializer = PostSubCategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    if req.method == "GET":
        query = SubCategory.objects.all()
        serializer = GetSubCategorySerializer(query, many=True)
        
        return Response(serializer.data, 200)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(req, id):
    try:
        sub_category = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response(status=404)
    
    query = Product.objects.filter(sub_category=id)
    serializer = SubProductSerializer(query, many=True)

    return Response(serializer.data, 200)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, id):

    try:
        sub_category = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response(status=404)
    
    if req.method == 'GET':
        sub_category_serializer = GetSubCategorySerializer(sub_category, many=False)
        return Response(sub_category_serializer.data)
    
    if req.method == 'DELETE':
        sub_category.delete()
        return Response(status=204)
         
    if req.method == 'PUT':
        serializer = PostSubCategorySerializer(sub_category, data=req.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        
        return Response(serializer.errors, status=400)