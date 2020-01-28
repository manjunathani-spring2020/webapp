from django.contrib import admin
from django.urls import path
from account.views import registration_view, api_detail_view, api_update_view
from bill.views import api_create_bill_post, api_detail_bill_view, api_delete_bill_view, api_update_blog_view, api_single_get_bill_view

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/user/', registration_view, name="register"),
    path('v1/user/self/get/', api_detail_view, name="get"),
    path('v1/user/self/put/', api_update_view, name="put"),
    path('bill/post/', api_create_bill_post, name="bill post"),
    path('bill/get/', api_detail_bill_view, name="bill get"),
    path('bill/delete/<uuid:uuid_bill_id>', api_delete_bill_view, name="bill delete"),
    path('bill/put/<uuid:uuid_bill_id>', api_update_blog_view, name="bill update"),
    path('bill/get/<uuid:uuid_bill_id>', api_single_get_bill_view, name="bill delete"),
]

