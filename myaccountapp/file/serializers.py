from rest_framework import serializers
from file.models import File


class FilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['url']


class FileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'uuid_file_id', 'url', 'upload_date']