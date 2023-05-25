from .models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from .serializers import CreateUserSerializer, ChangePasswordSerializer, UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken

def user_role(user):
    if user.isSuperuser: role = "admin"
    else: role = "client"

    return role


# Create your views here.
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

@api_view(['POST'])
def login_user(req):
    if req.method == "POST":
        try:
            user = User.objects.get(email=req.data["email"])
        except User.DoesNotExist:
            data = {
                "status": 404,
                "message": "No active account found with the given credentials",
                "code": "no_active_account"
            }
            return Response(data, data["status"])
        
        if user.check_password(req.data["password"]):
            token = RefreshToken.for_user(user)
            data = {
                'status': 200,
                'role': user_role(user),
                'refresh': str(token),
                'access': str(token.access_token)
            }
            return Response(data, data["status"])
        else:
            data = {
                "status": 400,
                "message": "Incorrect password",
                "code": "wrong_password"
            }
            return Response(data, data["status"])
     
@swagger_auto_schema(methods=['get', 'put', 'delete'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_update_delete_user(req):

    try:
        user = User.objects.get(email=req.user)
    except User.DoesNotExist:
        data = {
            "status": 404,
            "message": "Does not exist"
        }
        return Response(data, 404)
    
    if req.method == 'GET':

        serializer = UserSerializer(user)
        data = {
            "status": 200,
            "role": user_role(user),
            "data": serializer.data
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

        serializer = CreateUserSerializer(user, data=req.data)

        if serializer.is_valid():
            serializer.save()
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