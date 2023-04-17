from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics

from drf_yasg.utils import swagger_auto_schema

from .serializers import CreateUserSerializer, ChangePasswordSerializer

# Create your views here.
@swagger_auto_schema(method='post', request_body=CreateUserSerializer)
@api_view(['POST'])
def register_user(req):
    """
    An endpoint for creating user
    """
    if req.method=='POST':
        serializer = CreateUserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({"message": "proceed to login"}, status.HTTP_201_CREATED)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing user password
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)