from django.db.models import Q   

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from drf_yasg.utils import swagger_auto_schema

from ..serializers import PostSubCategorySerializer, CreateProductSerializer, GetCategorySubSerializer
from ..models import SubCategory, Product
from ..utils import Actions

@swagger_auto_schema(methods=['post', 'get'], request_body=PostSubCategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_get(req):

    OPTIONS = ['products', 'categories', 'sub_categories']

    if req.method == "POST":
        data, status = Actions.create(serializer=PostSubCategorySerializer, data=req.data)
    
    if req.method == "GET":
        
        query = req.GET.get('query')
        selection = req.GET.get('selection')
        
        if selection != None:
            if selection not in OPTIONS:
                return Response({'message': 'Invalid search selection'}, 400)

        data, status = Actions.get(serializer=GetCategorySubSerializer, model=SubCategory, 
                                   query=query, selection=selection, spy=Q)


    data = {
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_products(req, index):
    try:
        sub_category = SubCategory.objects.get(id=index)
    except SubCategory.DoesNotExist:
        return Response(status=404)
    
    query = Product.objects.filter(sub_category=sub_category.id)
    serializer = CreateProductSerializer(query, many=True)

    data = {
        "data": serializer.data
    }

    return Response(data, 200)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetCategorySubSerializer, model=SubCategory, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=SubCategory, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=PostSubCategorySerializer, model=SubCategory, index=index, data=req.data)

    data = {
        "data": data
    }
    
    return Response(data, status)