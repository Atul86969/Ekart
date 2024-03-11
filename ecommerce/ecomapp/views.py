from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order, MyOrder
from django.db.models import Q
from django.core.mail import send_mail
import random
import razorpay

# Create your views here.


def hello(request):
    return HttpResponse('first end point')


def base(request):
    return render(request, 'base.html')


def header(request):
    return render(request, 'header.html')


def footer(request):
    return render(request, 'footer.html')


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def contact(request):
    return render(request, 'contact.html')


def product_details(request, pid):
    p = Product.objects.filter(id=pid)
    context = {}
    context['data'] = p
    return render(request, 'product_details.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('uname')
        pwd = request.POST.get('upass')
        cpwd = request.POST.get('ucon')
        if name == '' or pwd == '' or cpwd == '':
            context['errmsg'] = 'Fields cannot be empty'
            return render(request, 'register.html', context)
        elif pwd != cpwd:
            context['notmatch'] = 'Password did not match'
            return render(request, 'register.html', context)
        else:
            u = User.objects.create(username=name, email=name)
            u.set_password(pwd)
            u.save()
            context['success'] = 'Registration Successfull'
            return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')


def user_login(request):
    context = {}
    if request.method == 'POST':
        user_name = request.POST['uname']
        upassword = request.POST['upass']
        if user_name == '' or upassword == '':
            context['errmsg'] = 'Fields cannot be empty'
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=user_name, password=upassword)
            if u is not None:
                login(request, u)
                print(request.user.is_authenticated)
                return redirect('/index')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/user_login')


def product(request):
    context = {}
    uid = request.user.id
    p = Product.objects.all()
    context['product'] = p
    return render(request, 'index.html', context)


def catfilter(request, cv):
    q1 = Q(catg=cv)
    q2 = Q(is_active=True)

    u = Product.objects.filter(q1 & q2)
    context = {}
    context['product'] = u
    return render(request, 'index.html', context)


def sortprice(request, sv):
    if sv == '1':
        p = Product.objects.order_by('-price').filter(is_active=True)
    else:
        p = Product.objects.order_by('price').filter(is_active=True)
    context = {}
    context['product'] = p
    return render(request, 'index.html', context)


def filterbyprice(request):
    min = request.GET['min']
    max = request.GET['max']
    # print(min,max)
    p = Product.objects.filter(price__gte=min, price__lte=max)
    context = {}
    context['product'] = p
    return render(request, 'index.html', context)


def cart(request, pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id)
        p = Product.objects.filter(id=pid)
        q1 = Q(userid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        context = {}
        context['data'] = p
        if n > 1:
            context['msg_alert'] = 'Product already exists in the cart !!'
            return render(request, 'product_details.html', context)
        else:
            c = Cart.objects.create(userid=u[0], pid=p[0])
            c.save()
            context['msg_success'] = 'Product sucessfully added to the cart !!'
            return render(request, 'product_details.html', context)
    else:
        return redirect('/user_login')


def viewcart(request):
    c = Cart.objects.filter(userid=request.user.id)
    tot = 0
    for x in c:
        tot = tot + x.pid.price * x.qty
    context = {}
    context['data'] = c
    context['tot'] = tot
    context['n'] = len(c)
    return render(request, 'cart.html', context)


def remove(request, cid):
    c = Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


def updateqty(request, x, cid):
    c = Cart.objects.filter(id=cid)
    q = c[0].qty
    if x == '1':
        q = q + 1
    elif q > 1:
        q = q - 1
    c.update(qty=q)

    return redirect('/viewcart')


def placeorder(request):
    c = Cart.objects.filter(userid=request.user.id)
    oid = random.randrange(1000, 9999)
    for x in c:
        amount = x.pid.price * x.qty
        o = Order.objects.create(
            order_id=oid, userid=x.userid, pid=x.pid, qty=x.qty, amt=amount
        )
        o.save()
        x.delete()
    return redirect('/fetchorder')


def fetchorder(request):
    o = Order.objects.filter(userid=request.user.id)
    tot = 0
    for x in o:
        tot = tot + x.amt
    context = {}
    context['data'] = o
    context['total'] = tot
    context['n'] = len(o)
    return render(request, 'placeorder.html', context)


def makepayment(request):
    client = razorpay.Client(
        auth=('rzp_test_R7kWkFU6ZllnWF', 'W0gE85soRmV6WanAQr1nW69n')
    )
    ord = Order.objects.filter(userid=request.user.id)
    tot = 0
    for x in ord:
        tot = tot + x.amt
        oid = x.order_id
    data = {'amount': tot * 100, 'currency': 'INR', 'receipt': oid}
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context['payment'] = payment
    return render(request, 'pay.html', context)


def paymentsuccess(request):
    sub = 'Ekart Order Status'
    msg = 'Thanks for Shopping'
    u = User.objects.filter(id=request.user.id)
    to = u[0]
    print(to)
    frm = 'atulyt86969@gmail.com'
    

    send_mail(sub, msg, frm, [to], fail_silently=False)
    ord = Order.objects.filter(userid=u[0])
    for x in ord:
        mo = MyOrder.objects.create(
            order_id=x.order_id, userid=x.userid, pid=x.pid, amt=x.amt, qty=x.qty
        )
        mo.save()
        x.delete()
    return HttpResponse('payment success')