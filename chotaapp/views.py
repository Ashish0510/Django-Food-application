from unicodedata import category
from django import views

from django.shortcuts import redirect, render,HttpResponseRedirect
from .models import Orderplaced, products,Cart,Customer
import uuid 
from django.core.mail import send_mail
from django.contrib import messages
from .forms import signupform
from .models import profile
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .forms import CustomeProfileform


# Create your views here.
def non_view(request):
 pro=products.objects.filter(category='non-veg')
 context={'pro':pro,'active':'btn-light'}
 return render(request,"chotaapp/non.html",context)


def veg_view(request):
 proo=products.objects.filter(category='veg')
 context1={'proo':proo,'active':'btn-light'}
 return render(request,"chotaapp/veg.html",context1)

def home_view(request):
    return render(request,'chotaapp/home.html',{'name':request.user})

def aut_signup(request):
 if request.method=="POST":
     fm=signupform(request.POST)
     if fm.is_valid():
         messages.success(request,"you have registered succesfully! Please verify the mail to activate your account")
         
         new_user=fm.save()  
         uid=uuid.uuid4()                 #
         pro_obj=profile(user=new_user,token=uid)  #
         pro_obj.save()   
         
         send_email_after_registration(new_user.email,uid)  
         return redirect("login")                      #
 else:
      fm=signupform()
 
 return render (request,"chotaapp/signup.html",{'form':fm})


def aut_login(request):
 if request.method=="POST":
         fm=AuthenticationForm(request=request,data=request.POST)
         if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
                    
            user=authenticate(username=uname, password=upass)
            pro=profile.objects.get(user=user)
            if pro.verify:
              if user is not None:
               login(request,user)
               messages.success(request,"login successfully")
             
               return HttpResponseRedirect("/")   
            else:
                messages.info(request,"Please verify your email first then login")  
                return redirect("login")       
 else:
     fm=AuthenticationForm()
 return render(request,"chotaapp/login.html",{'form':fm})


def aut_logout(request):
    logout(request)
    messages.success(request,"you are logged out successfully")
    return redirect('home')



def account_verify(request,token):
    pf=profile.objects.filter(token=token).first()
    pf.verify=True
    pf.save()
    return redirect("signup")

def send_email_after_registration(email,token):
    subject='Email verification'
    message=f'Hi click on the link to verify your Account http://127.0.0.1:8000/account-verify/{token}'
    from_email= settings.EMAIL_HOST_USER 
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)


def cart(request):
 if request.user.is_authenticated: 
    user=request.user
    product_id=request.GET.get('prod_id')
                                                                         
    item_already_in_cart= Cart.objects.filter(Q(product=product_id) & Q(user=user)).exists()         #
    if item_already_in_cart:  
        plus_cart(request)                                                                  #                                                           #
        return redirect("cartshow")                                                        #
    else:                                                                                             #
        
        product=products.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect("cartshow")
 else:
         messages.info(request,"Please login Or register first to access the cart")
         return redirect('home')

def cart_show(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        shipping_amount=40
        totalamount=0
        cart_product=[p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount
                context6={'carts':cart ,'amount':amount,'totalamount':totalamount}
            return render (request,'chotaapp/cart.html',context6)
        else:
            return render (request,'chotaapp/emptycart.html')
    else:
         messages.info(request,"Please login Or register first to access the cart")
         return redirect('home')


def plus_cart(request):
    if request.method =='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0
        shipping_amount=40
        totalamount=0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount

        data={'quantity':c.quantity,'amount':amount,'totalamount':totalamount}
        return JsonResponse(data)


def minus_cart(request):
    if request.method =='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0
        shipping_amount=40
        totalamount=0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount

        data={'quantity':c.quantity,'amount':amount,'totalamount':totalamount}
        return JsonResponse(data)

def remove_cart(request):
    if request.method =='GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0
        shipping_amount=40
        totalamount=0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount=(p.quantity*p.product.price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount

        data={'amount':amount,'totalamount':totalamount}
        return JsonResponse(data)
    


class profileview(views.View):
    def get(self,request):
        form=CustomeProfileform()
        return render(request,"chotaapp/profile.html",{'form':form,'active':'btn-primary'})

    def post(self,request):
        form=CustomeProfileform(request.POST)
        if form.is_valid():
             usr=request.user
             nm=form.cleaned_data["name"]
             em=form.cleaned_data["email"]
             ad=form.cleaned_data["address"]
             dis=form.cleaned_data["district"]
             st=form.cleaned_data["state"]
             pin=form.cleaned_data["pincode"]

             reg= Customer(user=usr,name=nm, email=em, address=ad, district=dis, state=st, pincode=pin  )
             reg.save()
             messages.success(request,"your details have been submitted successfully")

        return render(request,"chotaapp/profile.html",{'form':form,'active':'btn-primary','name':request.user})

def address(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    return render(request,"chotaapp/address.html",{'add':add,'active':'btn-primary'})

def checkout(request):
     user=request.user
     dat=Customer.objects.filter(user=user)
     quant=Cart.objects.filter(user=user)
     amount=0
     shipping_amount=40
     totalamount=0
     cart_product=[p for p in Cart.objects.all() if p.user == request.user]
     print(cart_product)
     if cart_product:
      for p in cart_product:
                tempamount=(p.quantity*p.product.price)
                amount=amount+tempamount
                totalamount=amount+shipping_amount

     cont={'dat':dat,'quant':quant,'totalamount':totalamount}
     return render(request,"chotaapp/checkout.html",cont)

def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


def orderplaced(request):
    user=request.user
    op=Orderplaced.objects.filter(user=user)
    return render(request,"chotaapp/orderplaced.html",{'op':op})







    













































































def send_email_after_registration(email,token):
    subject='Email verification'
    message=f'Hi click on the link to verify your Account http://127.0.0.1:8000/account-verify/{token}'
    from_email= settings.EMAIL_HOST_USER 
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
