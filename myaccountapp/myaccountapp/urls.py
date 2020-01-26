from django.contrib import admin
from django.urls import path
from account.views import registration_view, api_detail_view, api_update_view

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/user/', registration_view, name="register"),
    path('v1/user/self/get/', api_detail_view, name="get"),
    path('v1/user/self/put/', api_update_view, name="put"),
]

