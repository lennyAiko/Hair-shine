from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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

@swagger_auto_schema(methods=['post'], request_body=ProductItemSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(req):

    if ProductItem.objects.filter(product=req.data['product']).count() == 1:
        data = {
            "status": 400,
            "message": "Already exists"
        }   

        return Response(data, 400)

    query = create(req.user)

    price = Product.objects.get(id=req.data['product']).actual_price

    req.data["amount"] = price * int(req.data['quantity'])
    req.data["cart"] = query.id

    data, status = Actions.create(serializer=ProductItemSerializer, data=req.data)

    data = {
        "status": status,
        "data": data
    }

    return Response(data, status)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_item(req, index):

    if req.method == 'GET':
        data, status = Actions.get_single(serializer=GetProductItemSerializer, model=ProductItem, index=index)
    
    if req.method == 'DELETE':
        data, status = Actions.delete(model=ProductItem, index=index)
         
    if req.method == 'PUT':
        data, status = Actions.update(serializer=GetProductItemSerializer, model=ProductItem, index=index, data=req.data, item=True)

    data = {
        "status": status,
        "data": data
    }
    
    return Response(data, status)

@swagger_auto_schema(methods=['get'], request_body=CartSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empty_cart(req):

    req.user.cart.product_item.all().delete()

    data = {
        "status": 200,
        "message": "Cart is empty"
    }

    return Response(data, 200)