from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..serializers import CartSerializer, ProductItemSerializer, GetProductItemSerializer
from ..models import Cart, ProductItem, Product
from ..utils import Actions
from drf_spectacular.utils import extend_schema


def create(user):
    try:
        query = Cart.objects.get(user=user)
    except:
        Cart.objects.create(user=user)
        query = Cart.objects.get(user=user)

    return query


@extend_schema(responses=CartSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(req):

    query = create(req.user)

    serializer = CartSerializer(query, many=False)

    data, status = serializer.data, 200

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


@extend_schema(request=CartSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add(req):

    query = create(req.user)

    # product
    # total amount

    data, status = Actions.bulk(
        model=ProductItem, data=req.data, cart=query, second_model=Product)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)


# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def get_update_delete_item(req, index):

#     if req.method == 'GET':
#         data, status = Actions.get_single(
#             serializer=GetProductItemSerializer, model=ProductItem, index=index)

#     if req.method == 'DELETE':
#         data, status = Actions.delete(model=ProductItem, index=index)

#     if req.method == 'PUT':
#         data, status = Actions.update(
#             serializer=GetProductItemSerializer, model=ProductItem, index=index, data=req.data, item=True)

#     data = {
#         "status": status,
#         "data": data
#     }

#     return Response(data, status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empty_cart(req):

    req.user.cart.product_item.all().delete()

    data = {
        "status": 200,
        "message": "Cart is empty"
    }

    return Response(data, 200)
