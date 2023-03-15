
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
import json
from django.contrib.auth.models import User
from dms.authentication import SessionTokenAuthentication
from dms.permission import CustomPermission

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
def login_check(request):

    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    data = {}
    check_if_user_exists = User.objects.filter(username=username).exists()
    if check_if_user_exists:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_superuser:
                if user.is_active:
                    resp = {"status": True, "message": 'Login success'}
                    return Response(data=resp, status=status.HTTP_200_OK)
                else:
                    resp = {"status": False, "message": 'User not active'}
                    return Response(data=resp, status=status.HTTP_200_OK)
            else:
                    resp = {"status": False, "message": 'Use Customer login credencials'}
                    return Response(data=resp, status=status.HTTP_200_OK)
        else:
            resp = {"status": False, "message": 'Authentication failed'}
            return Response(data=resp, status=status.HTTP_200_OK)
    else:
        resp = {"status": False, "message": 'Invalid user'}
        return Response(data=resp, status=status.HTTP_200_OK)

@api_view(['GET'])
# @csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def UserRolePermissions(request):
    role_perm = {
        'id': request.user.id,
        'username': request.user.username,
        'role': request.role,
        'email' : request.email,
        'name' : request.user.first_name,
        'last_name' : request.user.last_name,
        'permissions': request.permissions,
        'customer_id': request.customer_id,
        'is_superuser': request.user.is_superuser,
        'customer_name':request.customer_name
    }
    return Response(role_perm)

