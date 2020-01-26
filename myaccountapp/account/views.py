from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from account.serializers import RegistrationSerializer, UserSerializer, UserSerializer2


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['uuid_id'] = account.uuid_id
            data['email'] = account.email
            data['first_name']= account.first_name
            data['last_name'] = account.last_name
            data['account_created'] = account.account_created
            data['account_updated'] = account.account_updated
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', PUT])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_detail_view(request):
    try:
        account = Account.objects.get(email=request.user)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(account)
        return Response(serializer.data)


@api_view(['PUT', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_update_view(request):
    try:
        account = Account.objects.get(email=request.user)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer2(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'successfully updated.'
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
