from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..serializers import CommentSerializer, GetCommentSerializer
from ..models import Product, Comment
from ..utils import Actions


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "POST":
        req.data['commenter'] = req.user.id
        data, status = Actions.create(
            serializer=CommentSerializer, data=req.data)

    if req.method == "GET":
        data, status = Actions.get(
            serializer=GetCommentSerializer, model=Comment, req=req)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(
            serializer=GetCommentSerializer, model=Comment, index=index)

    if req.method == 'DELETE':
        data, status = Actions.delete(model=Comment, index=index)

    if req.method == 'PUT':
        data, status = Actions.update(
            serializer=GetCommentSerializer, model=Comment, index=index, data=req.data)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)
