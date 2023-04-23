from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import PostSubCategorySerializer, GetSubCategorySerializer, SubProductSerializer
from ..models import SubCategory, Product
from ..utils import Actions

@swagger_auto_schema(methods=['post', 'get'], request_body=PostSubCategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        data, status = Actions.create(serializer=PostSubCategorySerializer, data=req.data)
    
    if req.method == "GET":
        data, status = Actions.get(serializer=GetSubCategorySerializer, model=SubCategory)

    return Response(data, status)

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
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetSubCategorySerializer, model=SubCategory, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=SubCategory, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=PostSubCategorySerializer, model=SubCategory, index=index, data=req.data)
    
    return Response(data, status)