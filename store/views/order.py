from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema

from ..serializers import OrderSerializer, GetOrderSerializer, ChargeSerializer, TransferSerializer
from ..models import Order
from ..utils import Actions, ReadOnly
import json, requests

info = open('keys.json',)
res = json.load(info)

BASE_URL = res["BASE_URL"]

def create(user):
    try:
        query = Order.objects.get(user=user)
    except:
        Order.objects.create(user=user)
        query = Order.objects.get(user=user)
    
    return query

@swagger_auto_schema(methods=['get'], request_body=OrderSerializer)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all(req):

    if req.user.role == "client":
        return Response({"message": "Does not exist", "status": 404}, 404)

    data, status = Actions.get(serializer=GetOrderSerializer, model=Order, req=req)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(methods=['get', 'post'], request_body=OrderSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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

        return Response(data, 200)
    
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
def webhook(req):

    if req.method != 'POST':
        return Response(status=403)
    
    if(len(req.headers['X-Paystack-Signature']) != 128): 
        return Response(status=403)
    
    if req.data['event'] == "charge.success":
        payload = {
            'event': req.data['event'],
            'reference':req.data['data']['reference'],
            'amount': req.data['data']['amount'],
            'status': req.data['data']['status'],
            'customer_email': req.data['data']['customer']['email'],
            'customer_code': req.data['data']['customer']['customer_code'],
        }

        serializer = ChargeSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    return Response(200)

SECRET_KEY = res["PAYSTACK_SECRET_KEY"]
OPTIONS = {"Authorization": f'Bearer {SECRET_KEY}', "Content-Type": "application/json"}

def post_requests(url, payload):
    payload = json.dumps(payload, indent=4) 
    res = requests.post(url=url, data=payload, headers=OPTIONS)
    res = res.json()

    return res

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_transfer(req):
    
    payload = {
        "email": str(req.data['email']),
        "amount": int(req.data['amount']) * 100
    }

    res = post_requests(f'{BASE_URL}/transaction/initialize', payload)

    return Response(res['data']['authorization_url'], 200)