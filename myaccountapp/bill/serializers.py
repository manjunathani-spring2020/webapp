from rest_framework import serializers
from bill.models import Bill


class BillSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Bill
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'payment_status']

    # def save(self):
    #     categories = self.validated_data['categories']
    #     print(categories)
    #
    #     if len(categories) != len(set(categories)):
    #         raise serializers.ValidationError({'categories': 'Values should be unique.'})
    #
    #     bill = Bill(vendor=self.validated_data['vendor'],
    #                 bill_date=self.validated_data['bill_date'],
    #                 due_date=self.validated_data['due_date'],
    #                 amount_due=self.validated_data['amount_due'],
    #                 categories=self.validated_data['categories'],
    #                 payment_status=self.validated_data['payment_status'],
    #                 owner_id=self.context.owner_id,
    #                 )
    #      self.context.vendor = self.validated_data['vendor']
    #     bill.save()
    #     return bill


class BillGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['vendor', 'uuid_bill_id', 'created_ts', 'updated_ts', 'owner_id', 'bill_date', 'due_date',
                  'amount_due', 'categories', 'payment_status']
