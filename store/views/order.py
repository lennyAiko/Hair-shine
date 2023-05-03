from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from ..serializers import OrderSerializer, GetOrderSerializer
from ..models import Order
from ..utils import Actions

def create(user):
    try:
        query = Order.objects.get(user=user)
    except:
        Order.objects.create(user=user)
        query = Order.objects.get(user=user)
    
    return query

@swagger_auto_schema(methods=['get'], request_body=OrderSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all(req):

    data, status = Actions.get(GetOrderSerializer, Order)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(methods=['get', 'post'], request_body=OrderSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_get(req):

    if req.method == "GET":
        query = Order.objects.filter(user=req.user)
        serializer = OrderSerializer(query, many=True)

        data, status = serializer.data, 200
        data = {
            "status": status,
            "data": data
        }

        return Response(data, status)
    
    if req.method == "POST":

        req.data['user'] = req.user.id

        data, status = Actions.create(serializer=OrderSerializer, data=req.data)

        data = {
            "status": status,
            "data": data
        }

        return Response("Successful", 200)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetOrderSerializer, model=Order, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=Order, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=GetOrderSerializer, model=Order, index=index, data=req.data)

    data = {
        "status": status,
        "data": data
    }
    
    return Response(data, status)