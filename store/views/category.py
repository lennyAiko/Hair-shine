from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CategorySerializer, GetCategorySubSerializer
from ..models import Category, SubCategory
from ..utils import Actions

# Create your views here.

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        data, status = Actions.create(serializer=CategorySerializer, data=req.data)
    
    if req.method == "GET":
        data, status = Actions.get(serializer=CategorySerializer, model=Category)

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subs(req, index):
    try:
        category = Category.objects.get(id=index)
    except Category.DoesNotExist:
        return Response(status=404)
    
    query = SubCategory.objects.filter(category=index)
    serializer = GetCategorySubSerializer(query, many=True)

    return Response(serializer.data, 200)


@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, index):
    
    if req.method == 'GET':
        data, status = Actions.get_single(serializer=CategorySerializer, model=Category, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Category, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CategorySerializer, model=Category, index=index, data=req.data)
    
    return Response(data, status)