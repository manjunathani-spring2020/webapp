import uuid
from django.db import models


def upload_location(instance, filename):
    file_path = 'bill/{file_id}-{filename}'.format(
        file_id=str(instance.uuid_file_id), filename=filename
    )
    return file_path


class File(models.Model):
    uuid_file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.FileField(upload_to=upload_location, null=False, blank=False)
    upload_date = models.DateField(auto_now_add=True, null=False, blank=False)
    file_name = models.CharField(max_length=50, null=True, blank=True)
    md5_sum = models.CharField(max_length=50, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.file_name
