from django.shortcuts import render,HttpResponse,redirect

from blog.models import review
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q

from django.db.models import Count
# Create your views here.

def commingsoon(request):
    return  render(request,'commingsoon.html')

def course_single(request,course):
    res={}
    crs=course_detail.objects.filter(slug=course)
    more_crs=course_detail.objects.all()
    if request.method=='POST':
        if request.user.is_authenticated:
            comment=request.POST['comment']
            rate=request.POST['rate']
            name=User.objects.get(id=request.user.id)
            crs=course_detail.objects.get(slug=course)
            rvw=crs_review(name=name,comment=comment,rate=rate,crs=crs)
            rvw.save()
            return redirect(request.get_full_path())
        else:
            return redirect ('login')
    rt_count=[]
    
    crs1=course_detail.objects.get(slug=course)
    rt=crs_review.objects.filter(crs=crs1).aggregate(Count('rate'))
    rt['id']=crs1.id
    rt_count.append(rt)
    count=crs_review.objects.filter(crs=crs1)
    print(count,'///////',rt_count,'pp',rt)

    ct_1=crs_review.objects.filter(crs=crs1,rate=1).count()
    ct_2=crs_review.objects.filter(crs=crs1,rate=2).count()
    ct_3=crs_review.objects.filter(crs=crs1,rate=3).count()
    ct_4=crs_review.objects.filter(crs=crs1,rate=4).count()
    ct_5=crs_review.objects.filter(crs=crs1,rate=5).count()
    
    res={'crs':crs,'more_crs':more_crs,'rate_count':rt_count,'count':len(count),'crss':count,'counts':(len(count)/5),
    'ct_1':ct_1,'ct_2':ct_2,'ct_3':ct_3,'ct_4':ct_4,'ct_5':ct_5}
    return  render(request,'course-single.html',res)

        
def courses(request):
    if request.method=='POST':
        search=request.POST['search']
        print(search,'ssssssssss')
        or_look=(Q(course_title__icontains=search)|Q(category__icontains=search)|Q(course_price__contains=search)|
        Q(course_description__icontains=search)|Q(slug__icontains=search)|Q(lession_no__icontains=search)
        |Q(student_no__icontains=search)|Q(course_certificate__icontains=search)|
        Q(course_quiz__icontains=search) |Q(course_duration_in_weeks__icontains=search))
        crs=course_detail.objects.filter(or_look).order_by('id')
    
    elif request.GET.get('inst')!=None:
        ins=instructor.objects.get(id=request.GET.get('inst'))
        crs=course_detail.objects.filter(course_instructor=ins).order_by('id')
    else:
        crs=course_detail.objects.all().order_by('id')
        
    res={'crs':crs,'count':course_detail.objects.all().count,'cnt':len(crs)}
    return  render(request,'courses.html',res)
