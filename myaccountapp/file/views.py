import os

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
        return Response({'response': "Bill doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill_obj.owner_id != request.user:
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill_obj.attachment is not None:
        return Response({'response': "Bill already has an attachment."},
                        status=status.HTTP_400_BAD_REQUEST)

    if not request_file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')):
        return Response({'response': "Bill already has to be pdf, png, jpg or jpeg."},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        serializer = FilePostSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            file = serializer.save()
            file.file_name = request_file_name
            file.file_size = request_file_size
            file.md5_sum = request_file_md5
            file.save()
            bill_obj.attachment = file
            bill_obj.save()

            data['response'] = 'successfully added a new file.'
            data['file_name'] = file.file_name
            data['id'] = file.uuid_file_id
            data['url'] = str(file.url)
            data['upload_date'] = file.upload_date
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def api_get_delete_file_view(request, uuid_bill_id, uuid_file_id):
    try:
        bill = Bill.objects.get(uuid_bill_id=uuid_bill_id)
        file = File.objects.get(uuid_file_id=uuid_file_id)
    except (Bill.DoesNotExist, File.DoesNotExist):
        return Response({'response': "Bill or File doesn't exist."},
                        status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        return Response({'response': "You don't have permissions to get/update/delete that bill."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FileGetSerializer(file)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        file_path = 'bill/{file_id}-{filename}'.format(
            file_id=str(file.uuid_file_id), filename=file.file_name
        )
        os.remove(os.path.join(settings.MEDIA_ROOT, file_path))
        operation = file.delete()
        data = {}
        if operation:
            data['response'] = 'successfully deleted the file.'
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
