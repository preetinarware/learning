
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from itertools import chain
from shop.models import*
from user_profile.models import*
from course.models import *
from blog.models import *
from event.views import *

from django.db.models import Count
from .models import*
# Create your views here.
def home(request):
    if request.method=="POST":
        email = request.POST['email1']
        var = Newsletter_subscriber(suscriber_email=email)
        var.save()
        return redirect('home')

    course=course_detail.objects.all()
    list={c.course_title for c in course}
    print(list,'ppppppp',len(list))
    blog=blog_detail.objects.all()
    inst=instructor.objects.all()
    res={'course':course,'blog':blog,'recent_crse':list,'instructor':inst}
    return  render(request,'index.html',res)


def search(request):
    next=request.get_full_path()
    if request.method=='POST':
        search=request.POST['search']
        crs=(Q(course_title__icontains=search)|Q(category__icontains=search)|Q(slug__icontains=search))

        blog=(Q(blog_category__icontains=search)|Q(blog_title__icontains=search)
        |Q(slug__icontains=search)|Q(tags__icontains=search))
        
        event=(Q(event_title__icontains=search)|Q(slug__icontains=search)|Q(where_event__icontains=search))
        
        shop_product=(Q(product_title__icontains=search)|Q(slug__icontains=search)|Q(product_tag__icontains=search) |Q(category__icontains=search))
         
        ints=(Q(name__icontains=search)|Q(slug__icontains=search)|Q(expert__icontains=search))
        
        crs=course_detail.objects.filter(crs)
        blg=blog_detail.objects.filter(blog).order_by('id')
        evnt=event_detail.objects.filter(event).order_by('id')
        shop=product_detail.objects.filter(shop_product).order_by('id')
        inst=instructor.objects.filter(ints).order_by('id')
    if len(crs)>0:
        paginator=Paginator(crs,6)
        page_no=request.GET.get('page')
        cors=paginator.get_page(page_no)
        res={'crs':cors,'count':course_detail.objects.all().count}
        return  render(request,'courses.html',res)

    elif len(blg)>0:
        li=[]
        cats=blog_detail.objects.values('blog_category')
        x={cat['blog_category'] for cat in cats}
        for i in x:
            cat=blog_detail.objects.filter(blog_category=i).count()
            li.append([i,cat])

        tag=blog_detail.objects.values('tags')
        tags={t['tags'] for t in tag}
        paginator=Paginator(blg,6)
        page_no=request.GET.get('page')
        page_obj=paginator.get_page(page_no)
        res={'blog':page_obj,'cat':li,'tag':tags}
        return  render(request,'blog.html',res)
    elif len(evnt)>0:
          
        paginator=Paginator(evnt,6)
        page_no=request.GET.get('page')
        page_obj=paginator.get_page(page_no)

        res={'event':page_obj}
        return render(request,'events.html',res)

    elif len(shop)>0:
        prod=product_detail.objects.all()
        rt_count=[]
        for p in prod:
            rt=shop_review.objects.filter(shop=p).aggregate(Count('rate'))
            rt['id']=p.id
            rt_count.append(rt)
   
        paginator=Paginator(shop,6)
        page_no=request.GET.get('page')
        products=paginator.get_page(page_no)

        res={'product':products,'rate_count':rt_count}
        return  render(request,'shop.html',res)

    elif len(inst)>0:
          return  render(request,'instructor.html',{'instructor':inst})

    return redirect('home')

def error(request):
    return render(request,'error-404.html')

def faqs(request):
    return  render(request,'faqs.html')

def gallery(request):
    return  render(request,'gallery.html')

def term_condition(request):
    return render(request,'term-condition.html')
def privacy(request):
     return render(request,'privacy-policy.html')