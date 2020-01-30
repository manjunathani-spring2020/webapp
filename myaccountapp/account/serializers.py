from rest_framework import serializers
from account.models import Account
import re


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self):
        account = Account(email=self.validated_data['email'],
                          first_name=self.validated_data['first_name'],
                          last_name=self.validated_data['last_name'],
                          )
        password = self.validated_data['password']

        flag = 0
        while True:
            if len(password) < 8:
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                print("Valid Password")
                break

        if flag == -1:
            raise serializers.ValidationError({'password': 'Password must be strong.'})

        account.set_password(password)
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['uuid_id', 'email', 'first_name', 'last_name', 'account_created','account_updated']


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = self.validated_data['password']

        flag = 0
        while True:
            if len(password) < 8:
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                print("Valid Password")
                break

        if flag == -1:
            raise serializers.ValidationError({'password': 'Password must be strong.'})

        instance.set_password(password)
        instance.save()
        return instance
