from django.contrib import admin
from django.urls import path
from account.views import registration_view, api_detail_get_put_view

from bill.views import api_create_bill_view, api_get_all_bills_view, api_get_put_delete_bill_view

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/user/', registration_view, name="register"),
    path('v1/user/self', api_detail_get_put_view, name="get and put"),
    path('v1/bill/', api_create_bill_view, name="bill post"),
    path('v1/bills', api_get_all_bills_view, name="bill get all"),
    path('v1/bill/<uuid:uuid_bill_id>', api_get_put_delete_bill_view, name="bill get put delete"),
]

