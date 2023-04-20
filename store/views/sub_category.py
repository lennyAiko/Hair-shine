from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import PostSubCategorySerializer, GetSubCategorySerializer
from ..models import SubCategory, Category

import json

@swagger_auto_schema(methods=['post'], request_body=PostSubCategorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(req):

    if req.method == "POST":
        
        serializer = PostSubCategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)

@swagger_auto_schema(method='get')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subcategories(req, id):

    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=404)

    query = SubCategory.objects.filter(category=category.id)
    serializer = GetSubCategorySerializer(query, many=True)

    return Response(serializer.data, 200)