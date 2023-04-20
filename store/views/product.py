from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import CreateProductSerializer
from ..models import Product, SubCategory

@swagger_auto_schema(methods=['post', 'get'], query_serializer=CreateProductSerializer)
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_get(req):
    if req.method == "POST":

        serializer = CreateProductSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    if req.method == "GET":
        query = Product.objects.all()
        serializer = CreateProductSerializer(query, many=True)
        
        return Response(serializer.data, 200)