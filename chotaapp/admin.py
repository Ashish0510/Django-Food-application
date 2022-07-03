from django.contrib import admin
from .models import products,profile,Cart,Customer,Orderplaced


# Register your models here.

class productsadmin(admin.ModelAdmin):
  list_display=['id','name']
admin.site.register(products,productsadmin)

@admin.register(profile)
class profileadmin(admin.ModelAdmin):
    list_display=["token","verify"]

class Cartadmin(admin.ModelAdmin):
  list_display=['user','product','quantity']


admin.site.register(Cart,Cartadmin)

class Customeradmin(admin.ModelAdmin):
  list_display=['id','name']
admin.site.register(Customer,Customeradmin)


class Orderplcedadmin(admin.ModelAdmin):
  search_fields=['user']
  list_filter=['user','product']
admin.site.register(Orderplaced,Orderplcedadmin)



