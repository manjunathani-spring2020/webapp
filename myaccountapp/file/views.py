import os
import logging
import django_statsd

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django_file_md5 import calculate_md5

from bill.models import Bill
from file.models import File
from file.serializers import FilePostSerializer, FileGetSerializer

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


@api_view(['POST'])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_upload_file_view(request, uuid_bill_id):
    request_file_name = request.data['url'].name
    request_file_md5 = calculate_md5(request.data['url'])
    request_file_size = request.data['url'].size

    try:
        bill_obj = Bill.objects.get(uuid_bill_id=uuid_bill_id)
    except Bill.DoesNotExist:
        logger.error("Bill Doesn't Exist")
        return Response({'response': "Bill doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill_obj.owner_id != request.user:
        logger.error("User Doesn't have permissions")
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill_obj.attachment is not None:
        logger.error("Bill already has an attachment")
        return Response({'response': "Bill already has an attachment."},
                        status=status.HTTP_400_BAD_REQUEST)

    if not request_file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        logger.error("Bill has to be pdf, png, jpg or jpeg")
        return Response({'response': "Bill already has to be pdf, png, jpg or jpeg."},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        django_statsd.incr('api.createFile')
        django_statsd.start('api.createFile.time.taken')
        serializer = FilePostSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            django_statsd.start('api.createFile.DB')
            file = serializer.save()
            file.file_name = request_file_name
            file.file_size = request_file_size
            file.md5_sum = request_file_md5
            file.save()
            bill_obj.attachment = file
            bill_obj.save()
            django_statsd.stop('api.createFile.DB')

            data['response'] = 'successfully added a new file.'
            data['file_name'] = file.file_name
            data['id'] = file.uuid_file_id

            if 'S3_BUCKET_NAME' in os.environ:
                data['url'] = str(file.url.url.split('?')[0])
            else:
                data['url'] = str(file.url)
            data['upload_date'] = file.upload_date
            logger.info("POST: Upload File")
            django_statsd.stop('api.createFile.time.taken')
            return Response(data, status=status.HTTP_201_CREATED)

        logger.error("ERROR: Something Happened: %s", serializer.errors)
        django_statsd.stop('api.createFile.time.taken')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_delete_file_view(request, uuid_bill_id, uuid_file_id):
    try:
        bill = Bill.objects.get(uuid_bill_id=uuid_bill_id)
        django_statsd.start('api.getFile.DB')
        file = File.objects.get(uuid_file_id=uuid_file_id)
        django_statsd.stop('api.getFile.DB')
    except (Bill.DoesNotExist, File.DoesNotExist):
        logger.error("Bill or File doesn't exist")
        return Response({'response': "Bill or File doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        logger.error("User You doesn't have permissions")
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        django_statsd.incr('api.getFile')
        django_statsd.start('api.getFile.time.taken')
        serializer = FileGetSerializer(file)
        logger.info("GET: Uploaded File")
        django_statsd.stop('api.getFile.time.taken')
        return Response(serializer.data)

    elif request.method == 'DELETE':
        django_statsd.incr('api.deleteFile')
        django_statsd.start('api.deleteFile.time.taken')

        if 'S3_BUCKET_NAME' in os.environ:
            django_statsd.start('s3.deleteFile.time.taken')
            file.url.delete(save=False)
            django_statsd.stop('s3.deleteFile.time.taken')
        else:
            file_path = 'bill/{file_id}-{filename}'.format(
                file_id=str(file.uuid_file_id), filename=file.file_name
            )
            os.remove(os.path.join(settings.MEDIA_ROOT, file_path))

        django_statsd.start('api.deleteFile.DB')
        operation = file.delete()
        django_statsd.stop('api.deleteFile.DB')

        data = {}
        if operation:
            data['response'] = 'successfully deleted the file.'
            logger.info("DELETE: Delete Uploaded File")
            django_statsd.stop('api.deleteFile.time.taken')
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
