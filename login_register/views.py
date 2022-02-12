from distutils.log import log
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from user_profile.models import instructor, student
from .models import *
import re
# Create your views here.


def loginregister(request):
    # next=request.META.get('HTTP_REFERER')
    
    return  render(request,'loginregister.html')

def register(request):
    if request.method == "POST":
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            confirm=request.POST['confirm']
            checkbox=request.POST.get('check')
            next=request.POST.get('next')
            
            usermail = User.objects.filter(email=email)
            usernam=User.objects.filter(username=name)
            if len(usermail) !=1 :
                if len(usernam)!=1:
                    # if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
      
                        user =User.objects.create_user(username=name, email=email, password=password)
                        user.save()
                        if checkbox != None:
                            typeuser = userType(user=user, type='1')
                            typeuser.save()
                            new_usr = name.replace(" ", "_")
                            inst=instructor(user=user,name=name,email=email,slug=new_usr)
                            inst.save()
                            token=str(uuid.uuid4())
                            frgpwd=frgt_pwd(user=user,frg_token=token)
                            frgpwd.save()
                            return redirect('home')
                        else:
                            typeuser = userType(user=user, type='2')
                            typeuser.save() 
                            new_usr = user.replace(" ", "_")
                            stud=student(user=user,name=name,email=email,slug=new_usr)
                            stud.save()
                            token=str(uuid.uuid4())
                            frgpwd=frgt_pwd(user=user,frg_token=token)
                            frgpwd.save()   
                            return redirect('home')
                    # return redirect('loginregister')
                return redirect('loginregister')
            return redirect('loginregister')
    return redirect('home')

    
def loged_in(request):
    if request.method=='POST':
            Email = request.POST['email']
            next=request.POST.get('next')
            user=User.objects.filter(email=Email)
            if len(user)==1 :
                username = User.objects.get(email=Email).username
                pwd = request.POST['password']
                user= authenticate(username=username,password=pwd)
                if user is not None:
                    login(request,user)
                    if next=='password-confirm' or next=='lost-password':
                        return redirect('home')
                    else:
                        return redirect(next)
               
    return redirect('loginregister')

def loged_out(request):
    logout(request)
    return redirect('home')
 

def lost_password(request):
    if request.user.is_authenticated!=True:
        if request.method=='POST':
            email=request.POST['email']
            useremail=User.objects.get(email=email)
            frgtoken=frgt_pwd.objects.get(user=useremail)
            ftoken=frgtoken.frg_token
            emails=useremail.email
            mail_msg=f'Your reset password link is http://127.0.0.1:8000/password-confirm/{ftoken}.'
            send_mail('For reset password', mail_msg,settings.EMAIL_HOST_USER, [emails],fail_silently=False)
            # messages.success(request, "mail send successfully. check your email. ")
            return redirect('lost-password')

        return render(request,'forgot-password.html')
    else:
        return redirect('error')
    

def pwd_reset_cnfrm(request,id):
    if request.user.is_authenticated!=True:
        if request.method=='POST':
            pass1=request.POST['pass1']
            confirm=request.POST['pass2']
            frgpwd=frgt_pwd.objects.get(frg_token=id)
            user=User.objects.get(username=frgpwd)
            user.set_password(pass1)
            user.save()
            # messages.success(request, "Password change successfully. ")/
            return redirect('login')
        
        return render(request,'pwd_reset_confirm.html')
    else:
        return redirect('error')