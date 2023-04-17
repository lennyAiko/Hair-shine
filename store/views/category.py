from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CategorySerializer
from ..models import Category

# Create your views here.

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CategorySerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":

        serializer = CategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    if req.method == "GET":
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data, 200)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=404)
    
    if req.method == 'GET':
        category_serializer = CategorySerializer(category, many=False)
        return Response(category_serializer.data)
    
    if req.method == 'DELETE':
        category.delete()
        return Response(status=204)
         
    if req.method == 'PUT':
        serializer = CategorySerializer(category, data=req.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=202)
        
        return Response(serializer.errors, status=400)