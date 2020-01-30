from rest_framework import serializers
from bill.models import Bill


class BillSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Bill
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'payment_status']


class BillGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['vendor', 'uuid_bill_id', 'created_ts', 'updated_ts', 'owner_id', 'bill_date', 'due_date',
                  'amount_due', 'categories', 'payment_status']
