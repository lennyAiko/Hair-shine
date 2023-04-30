from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from ..serializers import CartSerializer, ProductItemSerializer, GetProductItemSerializer
from ..models import Cart, ProductItem, Product
from ..utils import Actions

def create(user):
    try:
        query = Cart.objects.get(user=user)
    except:
        Cart.objects.create(user=user)
        query = Cart.objects.get(user=user)
    
    return query

@swagger_auto_schema(methods=['get'], request_body=CartSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get(req):

    query = create(req.user)
        
    serializer = CartSerializer(query, many=False)

    data, status = serializer.data, 200

    data = {
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(methods=['post'], request_body=ProductItemSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_item(req):

    if ProductItem.objects.filter(product=req.data['product']).count() == 1:
        return Response("Already exists", 400)

    query = create(req.user)

    price = Product.objects.get(id=req.data['product']).actual_price

    req.data["amount"] = price * int(req.data['quantity'])
    req.data["cart"] = query.id

    data, status = Actions.create(serializer=ProductItemSerializer, data=req.data)

    data = {
        "data": data
    }

    return Response("Successful", status)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetProductItemSerializer, model=ProductItem, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=ProductItem, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=GetProductItemSerializer, model=ProductItem, index=index, data=req.data, item=True)

    data = {
        "data": data
    }
    
    return Response(data, status)

#empty cart
# get user cart then run items.objects.all().delete()
@swagger_auto_schema(methods=['get'], request_body=CartSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def empty_cart(req):

    req.user.cart.product_item.all().delete()

    return Response(200)