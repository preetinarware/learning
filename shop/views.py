
from django.shortcuts import render,redirect
from django.db.models import Count
from login_register.views import register
from .models import *
from django.core.paginator import Paginator
from course.models import*
from blog.models import*
from datetime import date


# for pyment integration
from math import ceil
import json
from .paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
# from .checksum import  generate_checksum, verify_checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';

from django.contrib.auth.decorators import login_required
# Create your views here.
def shop(request):
    prod=product_detail.objects.all()
    rt_count=[]
    for p in prod:
        rt=shop_review.objects.filter(shop=p).aggregate(Count('rate'))
        rt['id']=p.id
        rt_count.append(rt)
   
    if request.GET.get('category') != None:
        product_detl=product_detail.objects.filter(category=request.GET.get('category'))
    elif request.GET.get('tag') != None:
        product_detl=product_detail.objects.filter(product_tag=request.GET.get('tag'))
    
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'menu_order':
        product_detl=product_detail.order_by('id')
    elif request.GET.get('orderby') != None and  request.GET.get('orderby') == 'popularity':
        product_detl=product_detail.objects.order_by('id')
    elif request.GET.get('orderby') != None and  request.GET.get('orderby') == 'price-desc':
        product_detl=product_detail.objects.order_by('-product_price')
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'date':
        product_detl=product_detail.objects.order_by('-id')
    elif request.GET.get('orderby') != None and request.GET.get('orderby') == 'price':
        product_detl=product_detail.objects.order_by('product_price')
   
    else:
        product_detl=product_detail.objects.order_by('id')

    paginator=Paginator(product_detl,6)
    page_no=request.GET.get('page')
    products=paginator.get_page(page_no)

    res={'product':products,'rate_count':rt_count,'count':product_detail.objects.all().count,'result_count':len(product_detl)}
    return  render(request,'shop.html',res)

def single_shop(request,shops):
    prod=product_detail.objects.all()
    product_detl=product_detail.objects.filter(slug=shops)
    rt_count=[]
    for p in prod:
        rt=shop_review.objects.filter(shop=p).aggregate(Count('rate'))
        rt['id']=p.id
        rt_count.append(rt)
    if request.method=='POST':
        if request.user.is_authenticated:
            review=request.POST['review']
            rate=request.POST['rate']
            usr=User.objects.get(id=request.user.id)
            shop=product_detail.objects.get(slug=shops)
            rvw=shop_review(shop=shop,review=review,rate=rate,user=usr)
            rvw.save()
            return redirect(request.get_full_path())
        else:
            return redirect('login')

    res={'product':product_detl,'rlt_product':prod,'rt_count':rt_count}
    return  render(request,'single-shop.html',res)

def mycart(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    li=[]
    res={}
    total=0

    dlt_item_id=request.GET.get('delete')
    slg=request.GET.get('slg')
    crt=cart.objects.filter(prod_id=dlt_item_id,slug=slg)
    crt.delete()
  
    for c in cartlist:
        prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
        crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
        
        if len(prod)>0:
            prod=product_detail.objects.get(id=c.prod_id)
            subtotal=prod.product_price*c.quntity
            total+=subtotal
            li.append([prod,c.quntity,subtotal])
        elif len(crs)>0:
            prod=course_detail.objects.get(id=c.prod_id)
            subtotal=prod.course_price*c.quntity
            total+=subtotal
            li.append([prod,c.quntity,subtotal])
    if request.method=='POST':
        cou_code=request.POST.get('coupon_code')
        cd=coupon_code.objects.filter(code=cou_code)
        if len(cd)>0:
            cod=coupon_code.objects.get(code=cou_code)
            for c in cartlist:
                c.coupon=cod.code 
                c.save()
                
            if cod.valid_date>date.today():
                cd=int((cod.discount*total)/100)
                total=total-cd
    
    res={'cart':li,'total':total}
    return  render(request,'cart.html',res)


def add_to_cart(request,addcart):
    if request.user.is_authenticated:
        carts=cart.objects.all()
        products=product_detail.objects.filter(slug=addcart)
        crs=course_detail.objects.filter(slug=addcart)   
        if len(products)==1:
            product=product_detail.objects.get(slug=addcart)
            prods=cart.objects.filter(prod_id=product.id,userid=request.user.id,slug=product.slug)
            if len(prods)>0:
                prod=prods[0]
                prod.quntity+=1
                prod.save()
            else:
                prod=cart.objects.create(slug=product.slug,userid=request.user.id,prod_id=product.id,prod_name=product.product_title,quntity=1)
        elif len(crs)==1:
            courses=course_detail.objects.get(slug=addcart)
            # crss=course_detail.objects.filter(slug=addcart,)
            prods=cart.objects.filter(prod_id=courses.id,userid=request.user.id,slug=courses.slug)
            if len(prods)>0:
                if len(prods)>0:
                    prod=prods[0]
                    prod.quntity=1
                    prod.save()
            else:
                prod=cart.objects.create(slug=courses.slug,userid=request.user.id,prod_id=courses.id,prod_name=courses.course_title,quntity=1)
        
        return redirect('cart')
    else:
        return redirect('loginregister')


def checkout(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    li=[]
    res={}
    total=0
    for c in cartlist:
        prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
        crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
        
        if len(prod)>0:
            prod=product_detail.objects.get(id=c.prod_id)
            subtotal=prod.product_price*c.quntity
            total+=subtotal
            li.append([prod,c.quntity,subtotal]) 
            cd=coupon_code.objects.filter(code=c.coupon)
            if len(cd)>0:
                cod=coupon_code.objects.get(code=c.coupon)
                if cod.valid_date>date.today():
                    cd=int((cod.discount*total)/100)
                    total=total-cd
                 
        elif len(crs)>0:
            prod=course_detail.objects.get(id=c.prod_id)
            subtotal=prod.course_price*c.quntity
            total+=subtotal
            cd=coupon_code.objects.filter(code=c.coupon)
            li.append([prod,c.quntity,subtotal])
            if len(cd)>0:
                cod=coupon_code.objects.get(code=c.coupon)
                if cod.valid_date>date.today():
                    cd=int((cod.discount*total)/100)
                    total=total-cd
            
        res={'cart':li,'total':total}
    return render(request, 'checkout.html',res)

def order(request):
    cartlist=cart.objects.filter(userid=request.user.id)
    li=[]
    res={}
    total=0
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        country=request.POST['country']
        address=request.POST['address']
        address2=request.POST.get('address2')
        city=request.POST['city']
        postal_code=request.POST['postal_code']
        province=request.POST['state']
        phone=request.POST['phone']
        payment_method=request.POST['payment_method']
        comapny=request.POST.get('company')
        order_notes=request.POST.get('order_notes')

        for c in cartlist:
            prod=product_detail.objects.filter(id=c.prod_id,slug=c.slug)
            crs=course_detail.objects.filter(id=c.prod_id,slug=c.slug)
            if len(prod)>0:
                prod=product_detail.objects.get(id=c.prod_id)
                subtotal=prod.product_price*c.quntity
                # total+=subtotal
                cd=coupon_code.objects.filter(code=c.coupon)
                if len(cd)>0:
                    cod=coupon_code.objects.get(code=c.coupon)
                    if cod.valid_date>date.today():
                        cd=int((cod.discount*subtotal)/100)
                        subtotal-=cd
          
                user=User.objects.get(id=c.userid)
                orders=product_order(product=prod,user=user,fname=fname,lname=lname,email=email,phone=phone,country=country,city=city,
                address=address+' '+address2,company=comapny,province=province,postal_code=postal_code,payment=payment_method,
                order_notes=order_notes,quntity=c.quntity,amount=subtotal,uid=uuid.uuid4())
                orders.save()
                # update = OrderUpdate(order_id=orders.id, update_desc="The order has been placed")
                # update.save()
                prods = product_detail.objects.filter(id=c.prod_id)
                qunt=prod.quntity-c.quntity
                if len(prods)>0:
                        ob=prods[0]
                        ob.quntity=qunt
                        ob.save()
                
                param_dict={
                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(orders.uid),
                'TXN_AMOUNT': str(format(subtotal,'.2f')),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/', }
                
                param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
                c.delete()
                return  render(request, 'paytms.html', {'param_dict': param_dict})
            
            elif len(crs)>0:
                crs=course_detail.objects.get(id=c.prod_id)
                subtotal=crs.course_price*c.quntity
                # total+=subtotal
                cd=coupon_code.objects.filter(code=c.coupon)              
                if len(cd)>0:
                    cod=coupon_code.objects.get(code=c.coupon)
                    if cod.valid_date>date.today():
                        cd=int((cod.discount*subtotal)/100)
                        subtotal-=cd
                user=User.objects.get(id=c.userid)
                orders=course_order(course=crs,user=user,fname=fname,lname=lname,email=email,phone=phone,country=country,city=city,
                address=address+' '+address2,company=comapny,province=province,postal_code=postal_code,payment=payment_method,
                order_notes=order_notes,quntity=c.quntity,amount=subtotal,uid=uuid.uuid4())
                orders.save()
                # update = OrderUpdate(order_id=orders.id, update_desc="The order has been placed")
                # update.save()
                crss = course_detail.objects.filter(id=c.prod_id)
                if len(crss)>0:
                        ob=crss[0]
                        ob.student_no+=1
                        ob.save()
                
                param_dict={
                    'MID': 'WorldP64425807474247',
                    'ORDER_ID': str(orders.uid),
                    'TXN_AMOUNT': str(format(subtotal,'.2f')),
                    'CUST_ID': email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/', 
                      }  
                param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
               
                c.delete()
                return  render(request, 'paytms.html', {'param_dict': param_dict})
            
    return redirect('checkout')

@csrf_exempt
def handle_request(request):
    print(request.user.id,'opppppppp')
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            inst=instructor.objects.filter(user=request.user.id)
            stud=student.objects.filter(user=request.user.id)
           
            print(stud,'[[[[',request.user.id,']]]]',inst)
            # if len(stud)>0:
            #     ob=stud[0]
            #     print(ob.slug,'[[[[')
            #     return redirect('profile',ob.slug)
            # elif len(inst)>0:
            #     ob=inst[0]
            #     print(ob.slug,'[[[[')
            #     return redirect('profile',ob.slug)
            return redirect('home')
       
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
     
    return render(request, 'paymentstatus.html', {'response': response_dict})


def purchase_guide(request):
    blg_tag=blog_detail.objects.values('tags')
    tag1={t['tags'] for t in blg_tag}

    prod_tag=product_detail.objects.values('product_tag')
    tag2={t['product_tag'] for t in prod_tag}
    tg=tag1.union(tag2)
    
    res={'tag':tg}
    
    return render(request,'purchase-guide.html',res)

def lp_checkout(request):
    return  render(request,'lp-checkout.html')


def detail(request,id):
    product_detl=product_detail.objects.filter(id=id)
    return redirect('shop',{'det':product_detl})


