"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from ecomapp import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),
    path('base/', views.base),
    path('index/',views.index),
    path('product_details/<pid>',views.product_details),
    path('register/',views.register),
    path('user_login/',views.user_login),
    path('user_logout/',views.user_logout),
    path('about/',views.about),
    path('contact/',views.contact),
    path('header/',views.header),
    path('footer/',views.footer),
    path('cart/<pid>',views.cart),
    path('placeorder/',views.placeorder),
    path('product/',views.product),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sortprice),
    path('filterbyprice/',views.filterbyprice),
    path('viewcart/',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment),
    path('paymentsuccess/',views.paymentsuccess),
    


]
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
