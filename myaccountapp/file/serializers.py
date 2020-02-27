from rest_framework import serializers
from file.models import File
import os


class FilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['url']


class FileGetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        if 'S3_BUCKET_NAME' in os.environ:
            return obj.url.url.split('?')[0]
        else:
            return obj.url

    class Meta:
        model = File
        fields = ['file_name', 'uuid_file_id', 'url', 'upload_date']
