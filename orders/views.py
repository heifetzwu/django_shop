from django.shortcuts import render, redirect

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .task import order_created
from .models import ORDER_PREFIX



def order_create(request):
    # get http get args from request
    # create a form instance and populate it with data from the request:
    args = request.GET.copy()
    if args.get("payby") is None:
        payby = ""
    else:
        payby = args.get("payby")
    
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            order = form.save()     # 我猜這個就是 insert 吧
            order.order_no = ORDER_PREFIX + str(order.id)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created(order.id)
            request.session['order_id'] = order.id
            # redirect to the payment
            
            if payby == "ecpay":
                
                return redirect('payment:process_ecpay')
            elif payby == "paypal":
                return redirect('payment:process_paypal')
        else:
            print ("@@@ form is not valid")
            print (form.errors)
            return redirect('cart:cart_detail')

    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
