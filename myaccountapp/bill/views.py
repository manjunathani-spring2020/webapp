from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from bill.models import Bill
from bill.serializers import BillSerializer, BillGetSerializer
from account.models import Account
import pdb


@api_view(['POST'])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_create_bill_view(request):
    bill_post = Bill(owner_id=request.user)
    account_user = Account.objects.get(email=request.user)

    if request.method == 'POST':
        serializer = BillSerializer(bill_post, data=request.data)
        data = {}
        if serializer.is_valid():

            categories_list = serializer.validated_data['categories']
            if len(categories_list) != len(set(categories_list)):
                return Response({'response': "Categories must be unique."},
                                status=status.HTTP_400_BAD_REQUEST)

            bill = serializer.save()
            data['response'] = 'successfully added a new bill.'
            data['uuid_bill_id'] = bill.uuid_bill_id
            data['created_ts'] = bill.created_ts
            data['updated_ts'] = bill.updated_ts
            data['owner_id'] = account_user.uuid_id
            data['vendor'] = bill.vendor
            data['bill_date'] = bill.bill_date
            data['due_date'] = bill.due_date
            data['amount_due'] = bill.amount_due
            data['categories'] = bill.categories
            data['payment_status'] = bill.payment_status
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_all_bills_view(request):
    try:
        account_user = Account.objects.get(email=request.user)
        bill = Bill.objects.all().filter(owner_id=account_user.uuid_id)
    except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BillGetSerializer(bill, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_put_delete_bill_view(request, uuid_bill_id):
    account_user = Account.objects.get(email=request.user)

    try:
        bill = Bill.objects.get(uuid_bill_id=uuid_bill_id)
    except Bill.DoesNotExist:
        return Response({'response': "Bill doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BillGetSerializer(bill)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BillSerializer(bill, data=request.data)
        data = {}
        if serializer.is_valid():
            categories_list = serializer.validated_data['categories']
            if len(categories_list) != len(set(categories_list)):
                return Response({'response': "Categories must be unique."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            data['response'] = 'successfully updated a new bill.'
            data['uuid_bill_id'] = bill.uuid_bill_id
            data['created_ts'] = bill.created_ts
            data['updated_ts'] = bill.updated_ts
            data['owner_id'] = account_user.uuid_id
            data['vendor'] = bill.vendor
            data['bill_date'] = bill.bill_date
            data['due_date'] = bill.due_date
            data['amount_due'] = bill.amount_due
            data['categories'] = bill.categories
            data['payment_status'] = bill.payment_status
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        operation = bill.delete()
        data = {}
        if operation:
            data['response'] = 'successfully deleted a new bill.'
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
