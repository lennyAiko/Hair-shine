from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CategorySerializer, GetCategorySubSerializer, GetCategoryProducts, CreateProductSerializer
from ..models import Category, SubCategory, Product
from ..utils import Actions, ReadOnly

# Create your views here.

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser|ReadOnly])
def create_get(req):

    OPTIONS = ['products', 'categories', 'sub_categories']

    if req.method == "POST":
        data, status = Actions.create(serializer=CategorySerializer, data=req.data)
    
    if req.method == "GET":
        query = req.GET.get('query')
        selection = req.GET.get('selection')
        
        if selection != None:
            if selection not in OPTIONS:
                return Response({'message': 'Invalid search selection'}, 400)

        data, status = Actions.get(serializer=CategorySerializer, model=Category, 
                                   query=query, selection=selection, spy=Q, req=req)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAdminUser|ReadOnly])
def get_subs(req, index):
    try:
        category = Category.objects.get(id=index)
    except Category.DoesNotExist:
        return Response(status=404)
    
    query = SubCategory.objects.filter(category=index)
    serializer = GetCategorySubSerializer(query, many=True)

    data = {
        "status": 200,
        "data": serializer.data
    }

    return Response(data, 200)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser|ReadOnly])
def get_update_delete(req, index):
    
    if req.method == 'GET':
        data, status = Actions.get_single(serializer=CategorySerializer, model=Category, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Category, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CategorySerializer, model=Category, index=index, data=req.data)
    
    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAdminUser|ReadOnly])
def get_products(req, index=None):
    store = []

    try:
        if type(index) == int:
            category = Category.objects.get(id=index)
        if type(index) == str:
            category = Category.objects.get(name=index)
    except:
        data = {
            "status": 404,
            "data": "Does not exist"
        }
        return Response(data, data['status'])

        
    serializer = GetCategoryProducts(category, many=False)

    for i in serializer.data['sub_category']:
        query = Product.objects.filter(sub_category=i)
        serializer = CreateProductSerializer(query, many=True)
        store.append(serializer.data)

    data = {
        "status": 200,
        "data": store
    }

    return Response(data, data['status'])