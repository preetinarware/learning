from django.contrib import admin
from .models import*
# Register your models here.
@admin.register(product_detail)
class product_detailAdmin(admin.ModelAdmin):
    list_display=['id','category','product_tag','product_title'[:20]]


@admin.register(shop_review)
class shop_review(admin.ModelAdmin):
    
    list_display_links=('shop','user','id')
    list_display=['id','user','shop'[:20],'rate','review']


@admin.register(cart)
class cart(admin.ModelAdmin):
    
    list_display_links=('userid','prod_name','id')
    list_display=['id','userid','prod_name','prod_id','quntity']


@admin.register(product_order)
class product_order(admin.ModelAdmin):
    
    list_display_links=('user',)
    list_display=['user','product','address','city','country']


@admin.register(course_order)
class course_order(admin.ModelAdmin):
    
    list_display_links=('user',)
    list_display=['user','course','address','city','country']


@admin.register(coupon_code)
class coupon_code(admin.ModelAdmin):
    
    list_display_links=('code','id')
    list_display=['id','code','valid_date','discount']
