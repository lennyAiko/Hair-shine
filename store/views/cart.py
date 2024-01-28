from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..serializers import CartSerializer, GetCartSerializer
from ..models import Cart, Product
from ..utils import Actions
from drf_spectacular.utils import extend_schema


def create(user):
    try:
        query = Cart.objects.get(user=user)
    except:
        Cart.objects.create(user=user)
        query = Cart.objects.get(user=user)

    return query


@extend_schema(request=CartSerializer, responses=GetCartSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_get(req):

    if req.method == "GET":

        query = create(req.user)

        serializer = GetCartSerializer(query, many=False)

        data, status = serializer.data, 200

        data = {
            "status": status,
            "data": data
        }

    if req.method == "POST":

        try:
            query = create(req.user)
            print(query)
            data, status = Actions.update(
                CartSerializer, Cart, query.id, req.data)
        except:
            req.data['user'] = req.user.id
            data, status = Actions.create(req.data, CartSerializer)

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

    cart = Cart.objects.get(user=req.user)

    print(cart)

    try:

        cart.delete()

        data = {
            "status": 200,
            "message": "Cart is empty"
        }

    except:
        data = {
            "status": 500,
            "message": "Something went wrong"
        }

    return Response(data, 200)
