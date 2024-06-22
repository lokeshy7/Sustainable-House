"""sustainable_house URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from client import views

urlpatterns = [
path('',views.BASEHOME,name="basehome"),
        path('client_login/',views.CLIENT_LOGIN,name="clientlogin"),
        path('client_register/',views.CLIENT_REG,name="clientregister"),
        path('client_home/',views.CLIENT_HOME,name="clienthome"),
        path('clientlogout/',views.CLIENTLOGOUT,name="clientlogout"),
        path('uploadrequirement/',views.UPLOADREQUIRE,name="upload"),

        path('uploadstructdetails/',views.UPSTRUCTDET),
        path('uploadintrequirement/',views.UPLOADINTREQUIREMENT),
        path('viewresults/',views.VIEWRESULT)

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
