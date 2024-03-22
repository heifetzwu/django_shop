from django.urls import path,re_path
from . import views
urlpatterns = [
    # re_path(r'^process/$', views.payment_process
    #     , name='process'),
    re_path(r'^process/$', views.payment_process_ecpay
        , name='process'),
    re_path(r'^process_ecpay/$', views.payment_process_ecpay
        , name='process_ecpay'),
    re_path(r'^process_paypal/$', views.payment_process_paypal
        , name='process_paypal'),
    re_path(r'^done/$', views.payment_done
        , name='done'),
    re_path(r'^canceled/$', views.payment_canceled
        , name='canceled'),
    re_path(r'^ecpay_return/$', views.ecpay_return
        , name='ecpay_return'),
    # path('ecpay_return', views.ecpay_return)
]
