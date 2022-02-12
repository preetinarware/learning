
from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator
from .models import*

from django.db.models import Q
# Create your views here.


def blog(request):
    if request.method=='POST':
        search=request.POST['search']
        look=(Q(blog_category__icontains=search)|Q(blog_title__icontains=search)
        |Q(slug__icontains=search)|Q(blog_description__icontains=search)|Q(tags__icontains=search)|Q(head1__icontains=search)
        |Q(head2__icontains=search)|Q(setting__icontains=search)|Q(why_need__icontains=search))
        blogs=blog_detail.objects.filter(look).order_by('id')  
    else:
      cat=request.GET.get('category')
      tg=request.GET.get('tags')
      if cat != None:
          blogs=blog_detail.objects.filter(blog_category=cat).order_by('id')
      elif tg != None:
          blogs=blog_detail.objects.filter(tags=tg).order_by('id')
      else:
        blogs=blog_detail.objects.all().order_by('id')

    li=[]
    cats=blog_detail.objects.values('blog_category')
    x={cat['blog_category'] for cat in cats}
    for i in x:
      cat=blog_detail.objects.filter(blog_category=i).count()
      li.append([i,cat])

    tag=blog_detail.objects.values('tags')
    tags={t['tags'] for t in tag}
    
    paginator=Paginator(blogs,6)
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no)
    res={'blog':page_obj,'cat':li,'tag':tags}
    return  render(request,'blog.html',res)

def single_blog(request,blogs):
    if request.GET.get('search')!= None :
        search=request.GET.get('search')
        look=(Q(blog_category__icontains=search)|Q(blog_title__icontains=search)
        |Q(slug__icontains=search)|Q(blog_description__icontains=search)|Q(tags__icontains=search)|Q(head1__icontains=search)
        |Q(head2__icontains=search)|Q(setting__icontains=search)|Q(why_need__icontains=search))
        blgs=blog_detail.objects.filter(look).order_by('id')  
    else:
       blgs=blog_detail.objects.filter(slug=blogs)
   



    blog_rcnt=blog_detail.objects.all() 
    li=[]
    cats=blog_detail.objects.values('blog_category')
    x={cat['blog_category'] for cat in cats}
    for i in x:
      cat=blog_detail.objects.filter(blog_category=i).count()
      li.append([i,cat])

    
    tag=blog_detail.objects.values('tags')
    tags={t['tags'] for t in tag}
    
    if request.method=='POST':
        if request.user.is_authenticated:
          comment=request.POST['comment']
          user=User.objects.get(id=request.user.id)
          bg=blog_detail.objects.get(slug=blogs)
          rvw=review(user=user,blog_id=bg,comment=comment)
          rvw.save()
          return redirect(request.get_full_path())
        else:
          return redirect('loginregister')

    res={'blog':blgs,'rcnt':blog_rcnt,'cat':li,'tag':tags}
    return  render(request,'single-blog.html',res)


    