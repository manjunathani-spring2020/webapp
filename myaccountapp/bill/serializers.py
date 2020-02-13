from rest_framework import serializers
from bill.models import Bill
from file.models import File


class BillSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Bill
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'payment_status']


class BillGetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'uuid_file_id', 'url', 'upload_date']

    def to_representation(self, instance):
        representation = super(BillGetFileSerializer, self).to_representation(instance)
        full_path = instance.url
        representation['url'] = full_path.name
        return representation


class BillGetSerializer(serializers.ModelSerializer):
    attachment = BillGetFileSerializer()

    class Meta:
        model = Bill
        fields = ['vendor', 'uuid_bill_id', 'created_ts', 'updated_ts', 'owner_id', 'bill_date', 'due_date',
                  'amount_due', 'categories', 'payment_status','attachment']
