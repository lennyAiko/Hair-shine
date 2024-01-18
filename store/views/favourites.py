from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..serializers import FavouriteSerializer, FavItemSerializer, GetFavItemSerializer
from ..models import FavItem, Favourite
from ..utils import Actions


def create(user):
    try:
        query = Favourite.objects.get(user=user)
    except:
        Favourite.objects.create(user=user)
        query = Favourite.objects.get(user=user)

    return query


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(req):

    query = create(req.user)

    serializer = FavouriteSerializer(query, many=False)

    data, status = serializer.data, 200

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(req):

    if FavItem.objects.filter(product=req.data['product']).count() == 1:
        data = {
            "status": 400,
            "data": "Item already exists"
        }
        return Response(data, 400)

    query = create(req.user)

    req.data["favourite"] = query.id

    data, status = Actions.create(serializer=FavItemSerializer, data=req.data)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(
            serializer=GetFavItemSerializer, model=FavItem, index=index)

    if req.method == 'DELETE':
        data, status = Actions.delete(model=FavItem, index=index)

    if req.method == 'PUT':
        data, status = Actions.update(
            serializer=GetFavItemSerializer, model=FavItem, index=index, data=req.data, item=True)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)
