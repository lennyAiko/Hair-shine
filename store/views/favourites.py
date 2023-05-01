from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

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

@swagger_auto_schema(methods=['get'], request_body=FavouriteSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get(req):

    query = create(req.user)
        
    serializer = FavouriteSerializer(query, many=False)

    data, status = serializer.data, 200

    data = {
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(methods=['post'], request_body=FavItemSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_item(req):

    if FavItem.objects.filter(product=req.data['product']).count() == 1:
        return Response("Already exists", 400)

    query = create(req.user)

    req.data["favourite"] = query.id

    data, status = Actions.create(serializer=FavItemSerializer, data=req.data)

    data = {
        "data": data
    }

    return Response("Successful", status)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetFavItemSerializer, model=FavItem, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=FavItem, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=GetFavItemSerializer, model=FavItem, index=index, data=req.data, item=True)

    data = {
        "data": data
    }
    
    return Response(data, status)