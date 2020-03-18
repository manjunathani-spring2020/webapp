import logging
from django_statsd.clients import statsd

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from account.serializers import RegistrationSerializer, UserSerializer, UserSerializer2

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        statsd.incr('api.registerUser')
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
            logger.info("POST: User Created with uuid: %s", account.uuid_id)
            return Response(data, status=status.HTTP_201_CREATED)
        logger.error("ERROR: Something Happened: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_detail_get_put_view(request):
    try:
        account = Account.objects.get(email=request.user)
    except Account.DoesNotExist:
        logger.error("User Doesn't Exist")
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        statsd.incr('api.getUser')
        serializer = UserSerializer(account)
        logger.info("GET: User with uuid: %s", account.uuid_id)
        return Response(serializer.data)
    elif request.method == 'PUT':
        statsd.incr('api.updateUser')
        serializer = UserSerializer2(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'successfully updated.'
            logger.info("PUT: User with uuid: %s", account.uuid_id)
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        logger.error("ERROR: Something Happened: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)