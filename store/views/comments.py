from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CommentSerializer
from ..models import Product, Comment
from ..utils import Actions

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CommentSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        data, status = Actions.create(serializer=CommentSerializer, data=req.data)
    
    if req.method == "GET":
        data, status = Actions.get(serializer=CommentSerializer, model=Comment)
    
    data = {
        "data": data
    }

    return Response(data, status)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=CommentSerializer, model=Comment, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Comment, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=CommentSerializer, model=Comment, index=index, data=req.data)
    
    data = {
        "data": data
    }
    
    return Response(data, status)