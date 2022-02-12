
import pytz
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import*
import datetime
import pytz


from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    res={}
    if request.method=='POST':
        if request.user.is_authenticated:
            name=request.POST['name']
            email=request.POST['email']
            subject=request.POST['subject']
            msg=request.POST['msg']
            user=User.objects.get(id=request.user.id)
            cont=contact_msg(user=user,name=name,email=email,subject=subject,Msg=msg)
            cont.save()
            
            send_mail(subject,msg,settings.EMAIL_HOST_USER,[email],fail_silently=False)
    
        else:
            return redirect('loginregister')
    if len(User.objects.filter(username='admin'))>0:
        usr=User.objects.get(username='admin')
        cont=contact_page_info.objects.filter(user=usr)
        res={'cont':cont}
    return  render(request,'contact.html',res)
