from decimal import Decimal

from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse


from orders.models import Order, OrderItem

# placeholder
import importlib.util, datetime, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
modfile = os.path.join(BASE_DIR, 'payment/ecpay_payment_sdk.py')

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    modfile
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def payment_process_ecpay(request):
    # prefix = "jackkkk"
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_id_ecpay = order.order_no
    host = request.get_host()
    scheme = request.is_secure() and "https" or "http"
    order_items = OrderItem.objects.filter(order_id = order_id)
    items = ""
    for i in order_items:
        items += i.product.name + " * " + str(i.quantity) + "#"
        
    order_params = {
            'MerchantTradeNo': order_id_ecpay,
            'StoreID': '',
            'MerchantTradeDate': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': order.get_total_cost(),
            'TradeDesc': order_id_ecpay,
            'ItemName': items, #['product_list'],
            # 'ReturnURL': f'{scheme}://{host}/{reverse("payment:done")}/', # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            # 'ReturnURL': f'{scheme}://{host}/orders/return/', # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            'ReturnURL': f'{scheme}://{host}{reverse("payment:ecpay_return")}', # ReturnURL為付款結果通知回傳網址，為特店server或主機的URL，用來接收綠界後端回傳的付款結果通知。
            
            'ChoosePayment': 'ALL',
            'ClientBackURL': f'{scheme}://{host}/', # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            # 'ClientBackURL': f'{scheme}://{host}/products/list/', # 消費者點選此按鈕後，會將頁面導回到此設定的網址(返回商店按鈕)
            'ItemURL': f'{scheme}://{host}/products/list/', # 商品銷售網址
            # 'ItemURL': f'{scheme}://{host}{reverse("payment:done")}/', # 商品銷售網址
            'Remark': '交易備註',
            'ChooseSubPayment': '',
            'OrderResultURL': f'{scheme}://{host}{reverse("payment:done")}', # 消費者付款完成後，綠界會將付款結果參數以POST方式回傳到到該網址
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': '',
            'CustomField2': '',
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
    # 建立實體
    ecpay_payment_sdk_backup = module.ECPayPaymentSdk(
            MerchantID='2000132',
            HashKey='5294y06JbISpM5x9',
            HashIV='v77hoKGq4kWxNNIS'
        )
    # ecpay_payment_sdk = module.ECPayPaymentSdk(
    #         MerchantID='3002607',
    #         HashKey='pwFHCqoQZGmho4w6',
    #         HashIV='EkRm7iFT261dpevs'
    #     )
    

    ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID = settings.ECPAY['MerchantID'],
            HashKey = settings.ECPAY['HashKey'],
            HashIV = settings.ECPAY['HashIV']
        )
    # 產生綠界訂單所需參數
    
    final_order_params = ecpay_payment_sdk.create_order(order_params)
    action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
    # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
    ecpay_form = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
    # context = self.get_context_data(**kwargs)
    context = {}
    context['ecpay_form'] = ecpay_form
    return render(request, 'payment/ecpay.html',context)


#

@csrf_exempt
def ecpay_return(request):
    ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID=settings.ECPAY['MerchantID'],
            HashKey=settings.ECPAY['HashKey'],
            HashIV=settings.ECPAY['HashIV']
        )
    
    res = request.POST.dict()
    back_check_mac_value = request.POST.get('CheckMacValue')
    
    check_mac_value = ecpay_payment_sdk.generate_check_value(res)
    
    if check_mac_value == back_check_mac_value:
        
        if res['RtnCode'] == '1':
            order_id_ecpay = res['MerchantTradeNo']
            order = get_object_or_404(Order, order_no=order_id_ecpay)
            order.paid = True
            order.save()
        return HttpResponse('0|Fail') # HttpResponse('1|OK') 
    return  HttpResponse('0|Fail')
    
    
    return render(request, 'payment/ecpay_return.html')


def payment_process_paypal(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'TWD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
                  'payment/process.html',
                  {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
