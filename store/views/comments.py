from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CommentSerializer
from ..models import Product, Comment

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CommentSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):
    if req.method == "POST":

        serializer = CommentSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    if req.method == "GET":
        query = Comment.objects.all()
        serializer = CommentSerializer(query, many=True)
        
        return Response(serializer.data, 200)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response(status=404)
    
    if req.method == 'GET':
        comment_serializer = CommentSerializer(comment, many=False)
        return Response(comment_serializer.data)
    
    if req.method == 'DELETE':
        comment.delete()
        return Response(status=204)
         
    if req.method == 'PUT':
        comment_serializer = CommentSerializer(comment, data=req.data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=202)
        
        return Response(comment_serializer.errors, status=400)