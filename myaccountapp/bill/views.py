import os
import logging
import django_statsd
from celery import shared_task
from datetime import datetime, timedelta, date
import pdb

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from bill.models import Bill
from bill.serializers import BillSerializer, BillGetSerializer
from account.models import Account
from file.models import File

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


@api_view(['POST'])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_create_bill_view(request):
    bill_post = Bill(owner_id=request.user)
    account_user = Account.objects.get(email=request.user)

    if request.method == 'POST':
        django_statsd.incr('api.createBill')
        django_statsd.start('api.createBill.time.taken')
        serializer = BillSerializer(bill_post, data=request.data)
        data = {}
        if serializer.is_valid():

            categories_list = serializer.validated_data['categories']
            if len(categories_list) != len(set(categories_list)):
                return Response({'response': "Categories must be unique."},
                                status=status.HTTP_400_BAD_REQUEST)
            django_statsd.start('api.createBill.db')
            bill = serializer.save()
            django_statsd.stop('api.createBill.db')
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
            logger.info("POST: Added Bill")
            django_statsd.stop('api.createBill.time.taken')
            return Response(data, status=status.HTTP_201_CREATED)

        logger.error("ERROR: Something Happened: %s", serializer.errors)
        django_statsd.stop('api.createBill.time.taken')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_all_bills_view(request):
    try:
        django_statsd.start('api.getAllBills.DB')
        account_user = Account.objects.get(email=request.user)
        bill = Bill.objects.all().filter(owner_id=account_user.uuid_id)
        django_statsd.stop('api.getAllBills.DB')
    except Bill.DoesNotExist:
        logger.error("Bill Doesn't Exist")
        django_statsd.stop('api.getAllBills.DB')
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        django_statsd.incr('api.getAllBills')
        django_statsd.start('api.getAllBills.time.taken')
        serializer = BillGetSerializer(bill, many=True)
        logger.info("GET: All Bills for User with uuid: %s", account_user.uuid_id)
        django_statsd.stop('api.getAllBills.time.taken')
        return Response(serializer.data)


@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_due_bills_view(request, days):
    try:
        account_user = Account.objects.get(email=request.user)
        due_date = date.today() + timedelta(days=days)
        bill = Bill.objects.all().filter(owner_id=account_user.uuid_id).filter(due_date__range=(date.today(), due_date))
    except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BillGetSerializer(bill, many=True)
        get_bill_due_sqs.delay(serializer.data)
        type(serializer.data)
        pdb.set_trace()
        return Response(serializer.data)


@shared_task
def get_bill_due_sqs(data):
    return data


@api_view(['GET', 'PUT', 'DELETE', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_put_delete_bill_view(request, uuid_bill_id):
    account_user = Account.objects.get(email=request.user)

    try:
        django_statsd.start('api.getBill.DB')
        bill = Bill.objects.get(uuid_bill_id=uuid_bill_id)

        if bill.attachment is not None:
            file = File.objects.get(uuid_file_id=bill.attachment.uuid_file_id)
        django_statsd.stop('api.getBill.DB')

    except Bill.DoesNotExist:
        logger.error("Bill Doesn't Exist")
        django_statsd.stop('api.getBill.DB')
        return Response({'response': "Bill doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        logger.error("User Doesn't have permissions")
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        django_statsd.incr('api.getBill')
        django_statsd.start('api.getBill.time.taken')
        serializer = BillGetSerializer(bill)
        django_statsd.stop('api.getBill.time.taken')
        return Response(serializer.data)

    elif request.method == 'PUT':
        django_statsd.incr('api.putBill')
        django_statsd.start('api.putBill.time.taken')
        serializer = BillSerializer(bill, data=request.data)
        data = {}
        if serializer.is_valid():
            categories_list = serializer.validated_data['categories']
            if len(categories_list) != len(set(categories_list)):
                return Response({'response': "Categories must be unique."},
                                status=status.HTTP_400_BAD_REQUEST)
            django_statsd.start('api.putBill.DB')
            serializer.save()
            django_statsd.stop('api.putBill.DB')
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
            logger.info("PUT: Update Bill for User")
            django_statsd.stop('api.putBill.time.taken')
            return Response(data=data, status=status.HTTP_200_OK)

        logger.error("ERROR: Something Happened: %s", serializer.errors)
        django_statsd.stop('api.putBill.time.taken')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        django_statsd.incr('api.deleteBill')
        django_statsd.start('api.deleteBill.time.taken')

        if bill.attachment is not None:
            if 'S3_BUCKET_NAME' in os.environ:
                django_statsd.start('s3.deleteBill.File.time.taken')
                bill.attachment.url.delete(save=False)
                django_statsd.stop('s3.deleteBill.File.time.taken')
            else:
                file_path = 'bill/{file_id}-{filename}'.format(
                    file_id=str(file.uuid_file_id), filename=file.file_name
                )
                os.remove(os.path.join(settings.MEDIA_ROOT, file_path))

        django_statsd.start('api.deleteBill.DB')
        operation = bill.delete()
        django_statsd.stop('api.deleteBill.DB')
        data = {}
        if operation:
            data['response'] = 'successfully deleted a new bill.'
            logger.info("DELETE: Bill deleted")
            django_statsd.stop('api.deleteBill.time.taken')
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
