from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from .serializers import CreateUserSerializer, ChangePasswordSerializer, ProfileSerializer, UserSerializer

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
        
        return Response({"status": 201, "message": "proceed to login"}, 201)

@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_user(req):

    role = ""

    try:
        user = req.user
    except User.DoesNotExist:
        data = {
            "status": 404,
            "message": "Does not exist"
        }
        return Response(data, 404)
    
    if req.method == 'GET':
        profile_serializer = ProfileSerializer(user.profile)

        if user.is_superuser: 
            role = "Admin"
            print(role)
        else: role = "Client"

        data = {
            "status": 200,
            "role": role,
            "data": profile_serializer.data
        }

        return Response(data, 200)
    
    if req.method == 'DELETE':
        user.delete()
        data = {
            "status": 204,
            "message": "Delete successful"
        }
        return Response(data, 204)
         
    if req.method == 'PUT':
        try:
            user.profile.location = req.data['location']
        except:
            user.profile.location = user.profile.location

        try:
            email = req.data['email']
        except:
            email = user.email

        data = {
            "username": req.user.username,
            "email": email
        }

        serializer = UserSerializer(user, data=data)

        if serializer.is_valid():
            serializer.save()
            user.profile.save()
            serializer = ProfileSerializer(user.profile)
            data = {
                "status": 202,
                "data": serializer.data
            }

            return Response(data, 202)
        
        return Response(serializer.errors, 400)

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
                return Response({"old_password": ["Wrong password."]}, 400)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': 200,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, 400)