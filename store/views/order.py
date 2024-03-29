from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..serializers import OrderSerializer, GetOrderSerializer, GetCartSerializer
# TransactionSerializer
from ..models import Order, Cart
from ..utils import Actions, ReadOnly
import json
import requests
from decouple import config
from drf_spectacular.utils import extend_schema

SECRET_KEY = config('SECRET_KEY')
HYDROGEN_TEST_URL = config('HYDROGEN_TEST_URL')
HYDROGEN_LIVE_URL = config('HYDROGEN_LIVE_URL')
HYDROGEN_USERNAME = config('HYDROGEN_USERNAME')
HYDROGEN_PASSWORD = config('HYDROGEN_PASSWORD')
HYDROGEN_API_KEY = config('HYDROGEN_API_KEY')
OPTIONS = {"authorization": HYDROGEN_API_KEY,
           "Content-Type": "application/json"}


def post_requests(url, payload):
    payload = json.dumps(payload, indent=4)
    res = requests.post(url=url, data=payload, headers=OPTIONS)
    res = res.json()

    return res


def create(user):
    try:
        query = Order.objects.get(user=user)
    except:
        Order.objects.create(user=user)
        query = Order.objects.get(user=user)

    return query


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products(req):
    user = req.user
    data = list(Cart.objects.get(user=user).product.all().values())
    return Response(data, 200)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all(req):

    if req.user.role == "client":
        return Response({"message": "Does not exist", "status": 404}, 404)

    data, status = Actions.get(
        serializer=GetOrderSerializer, model=Order, req=req)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@extend_schema(request=OrderSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "GET":

        query = Order.objects.filter(user=req.user.id)
        serializer = OrderSerializer(query, many=True)

        data, status = serializer.data, 200
        # cart_data = cart_serializer.data
        data = {
            "status": status,
            "order": data,
            "products": list(req.user.cart.product.all().values())

        }

        return Response(data, status)

    if req.method == "POST":

        req.data['user'] = req.user.id
        req.data['products'] = list(Cart.objects.get(
            user=req.user.id).product.all().values())

        data, status = Actions.create(
            serializer=OrderSerializer, data=req.data)

        if status == 201:

            payload = {
                "email": str(req.user.email),
                "amount": int(req.data['amount']),
                "callback": "https://www.hairsenseretail.com/my_account",
                "currency": "NGN",
                "description": "Payment for HairSense Retail",
                "meta": "test meta",
            }

            res = post_requests(
                f'{HYDROGEN_TEST_URL}/merchant/initiate-payment', payload)

            return Response(
                {
                    # "data": {"url": res['data']['url'] if res['data']['url'] else ""},

                    "message": "Successfully fetched payment URL"
                },
                200)

        data = {
            "status": 500,
            "data": "Could not contact server"
        }

        req.user.cart.product.all().delete()

        return Response(data, 500)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(
            serializer=GetOrderSerializer, model=Order, index=index)

    if req.method == 'DELETE':
        data, status = Actions.delete(model=Order, index=index)

    if req.method == 'PUT':
        data, status = Actions.update(
            serializer=GetOrderSerializer, model=Order, index=index, data=req.data)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@api_view(['POST'])
def webhook(req):

    if req.method != 'POST':
        return Response(status=403)

    order = Order.objects.get(user=req.data["customerEmail"])

    payload = {
        'transaction_status': req.data['status'],
        'transaction_id': req.data['data']['transactionRef'],
        'payment_type': req.data['paymentType'],
        'amount': req.data['amount'],
    }

    data, status = Actions.update(OrderSerializer, Order, order.id, payload)
    # serializer = TransactionSerializer(data=payload)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()

    return Response(200)


@api_view(['POST'])
def confirm_payment(req):

    transaction_ref = req.data["reference"]

    res = post_requests(
        "https://qa-api.hydrogenpay.com/bepayment/api/v1/Merchant/confirm-payment", transaction_ref)

    return Response(
        {
            "message": res["message"],
            "status": 200,
            "data": {
                "amount": res["data"]["amount"],
                "customerEmail": res["data"]["customerEmail"],
                "status": res["data"]["status"],
                "paymentType": res["data"]["paymentType"],
            }
        }, 200)
