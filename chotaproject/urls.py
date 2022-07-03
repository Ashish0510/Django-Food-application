"""chotaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.contrib import admin
from django.urls import include, path
from chotaapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('nonveg', views.non_view,name='nonveg'),
    path('veg/', views.veg_view,name='veg'),
    path('signup', views.aut_signup,name='signup'),
    path('login', views.aut_login,name='login'),
    path('profile', views.profileview.as_view(),name='profile'),
    path('aut_logout', views.aut_logout,name='logout'),
    path ('account-verify/<slug:token>',views.account_verify,name='account_verify'),
    path('', views.home_view,name='home'),
    path('add-to-cart', views.cart,name='add-to-cart'),
    path('checkout', views.checkout,name='checkout'),
    path('cartshow', views.cart_show,name='cartshow'),
    path('pluscart', views.plus_cart,name='pluscart'),
    path('minuscart', views.minus_cart,name='minuscart'),
    path('removecart', views.remove_cart,name='removecart'),
    path('address', views.address,name='address'),
    path('paymentdone', views.payment_done,name='paymentdone'),
    path('orders', views.orderplaced,name='orders'),
    
]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)