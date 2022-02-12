from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth.models import User
from course.models import course_detail
from shop.models import course_order, product_order
from user_profile.models import instructor, student



# Create your views here.

def private_message(request,msg):
    
    instruct=instructor.objects.filter(slug=msg)
    res={'instruct':instruct}

    return  render(request,'priveate-message.html',res)

def profile_certificates(request,certificate):
    li=[]
    instruct=instructor.objects.filter(slug=certificate)
    stud=student.objects.filter(slug=certificate)
    
    if len(instruct)>0:
        res={'instruct':instruct}
    elif len(stud)>0:
        res={'instruct':stud}
    if len(instruct)>0:
        usr=instructor.objects.get(user=User.objects.get(id=request.user.id))
        cr=course_detail.objects.filter(course_instructor=usr)
        for c in cr:
            if c.course_certificate!= '':
                li.append(c)
        print(c.course_certificate,'ppppp',li)
        res['crtfct']=li
    return  render(request,'profile-certificates.html',res)

def setting_genralinfo(request,genralinfo):
    if request.user.is_authenticated:
        nxt=request.get_full_path()
        instruct=instructor.objects.filter(slug=genralinfo)
        stud=student.objects.filter(slug=genralinfo)

        if request.method=='POST':
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                name = request.POST.get('name')
                email = request.POST.get('email')
                about=request.POST.get('about')
                fb_social=request.POST.get('fb_social')
                tw_social=request.POST.get('tw_social')
                li_social=request.POST.get('li_social')
                yt_social=request.POST.get('yt_social')   
                user=User.objects.get(id=request.user.id)
                user.first_name = fname
                user.last_name = lname
                user.save()
                if len(instruct)>0: 
                    inst=instruct[0]
                    inst.user=user
                    inst.name=name
                    inst.email=email
                    inst.about=about
                    inst.facebook=fb_social
                    inst.twitter=tw_social
                    inst.youtube=yt_social
                    inst.linkedin=li_social
                    inst.save()
                    return redirect(request.get_full_path())
                elif len(stud)>0: 
                        st=stud[0]
                        st.user=user
                        st.name=name
                        st.email=email
                        st.about=about
                        st.facebook=fb_social
                        st.twitter=tw_social
                        st.youtube=yt_social
                        st.linkedin=li_social
                        st.save()
                        return redirect(request.get_full_path())
                else:
                    return redirect(nxt)
        if len(instruct)>0:
            res={'instruct':instruct}
        elif len(stud)>0:
            res={'instruct':stud}
    
        return  render(request,'setting-genralinfo.html',res)
    else:
        return redirect('error')


def settings_avatar(request,avatar):
    
    if request.user.is_authenticated:
        instruct=instructor.objects.filter(slug=avatar)
        stud=student.objects.filter(slug=avatar)

        if request.method=='POST':
            img = request.FILES['img'] 
            if len(instruct)>0: 
                inst=instruct[0]
                inst.img=img
                inst.save()
            elif len(stud)>0: 
                st=stud[0]
                st.img=img
                st.save()
        if len(instruct)>0:
            res={'instruct':instruct}
        elif len(stud)>0:
            res={'instruct':stud}
        
        
        return  render(request,'settings-avatar.html',res)
    else:
        return redirect('error')

    
def settings_privacy(request,privacy):
    
    if request.user.is_authenticated:    
        instruct=instructor.objects.filter(slug=privacy)
        stud=student.objects.filter(slug=privacy)
        if len(instruct)>0:
            res={'instruct':instruct}
        elif len(stud)>0:
            res={'instruct':stud}

        

        return  render(request,'settings-privacy.html',res)
    else:
        return redirect('error')
        

def profile(request,profile):
    
        instruct=instructor.objects.filter(slug=profile)
        stud=student.objects.filter(slug=profile)
        if len(instruct)>0:
            res={'instruct':instruct}
        elif len(stud)>0:
            res={'instruct':stud}

        return  render(request,'profile.html',res)
   
def success_story(request):
    return  render(request,'success-story.html')


def instructors(request):
    inst=instructor.objects.all()
    res={'instructor':inst}
    return  render(request,'instructor.html',res)


def orders(request,order):
     
    instruct=instructor.objects.filter(slug=order)
    stud=student.objects.filter(slug=order)
    if len(instruct)>0:
        res={'instruct':instruct}
    elif len(stud)>0:
        res={'instruct':stud}
    c=User.objects.get(id=request.user.id)
    res['crs_oder']=course_order.objects.filter(user=c)
    res['prod_oder']=product_order.objects.filter(user=c)
    return  render(request,'orders.html',res)


def quzess(request,quize):
    
    
    instruct=instructor.objects.filter(slug=quize)
    stud=student.objects.filter(slug=quize)
    
    if len(instruct)>0:
        res={'instruct':instruct}
    elif len(stud)>0:
        res={'instruct':stud}

    return  render(request,'quzess.html',res)
