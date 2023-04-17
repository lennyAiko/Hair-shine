from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from ..serializers import SubCategorySerializer
from ..models import SubCategory, Category

@swagger_auto_schema(methods=['post'], req=SubCategorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_get(req):

    # try:
    #     category = Category.objects.get(id=id)
    # except Category.DoesNotExist:
    #     return Response(status=404)

    if req.method == "POST":
        
        serializer = SubCategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)
    
    # if req.method == "GET":
    #     query = SubCategory.objects.all(category=category)
    #     serializer = SubCategory(query, many=True)
    #     return Response(serializer.data, 200)