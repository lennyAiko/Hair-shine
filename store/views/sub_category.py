from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import PostSubCategorySerializer, GetSubCategorySerializer, SubProductSerializer
from ..models import SubCategory, Category

@swagger_auto_schema(methods=['post'], request_body=PostSubCategorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(req):

    if req.method == "POST":
        
        serializer = PostSubCategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subcategories(req, id):

    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=404)

    query = SubCategory.objects.filter(category=category.id)
    serializer = GetSubCategorySerializer(query, many=True)

    return Response(serializer.data, 200)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(req, id):
    try:
        sub_category = SubCategory.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=404)
    
    query = sub_category.product.all()
    serializer = SubProductSerializer(query, many=True)

    return Response(serializer.data, 200)

# @swagger_auto_schema(methods=['get', 'put', 'delete'])
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def get_update_delete(req, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response(status=404)
    
#     if req.method == 'GET':
#         category_serializer = CategorySerializer(category, many=False)
#         return Response(category_serializer.data)
    
#     if req.method == 'DELETE':
#         category.delete()
#         return Response(status=204)
         
#     if req.method == 'PUT':
#         serializer = CategorySerializer(category, data=req.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=202)
        
#         return Response(serializer.errors, status=400)