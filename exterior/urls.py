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
from exterior import views

urlpatterns = [
path('exterior_log/',views.EXTERIORLOG,name="exteriorlog"),
        path('exterior_reg/',views.EXTERIORREG,name="exteriorreg"),
        path('exterior_home/',views.EXTERIORHOME,name="exteriorhome"),
        path('ext_logout/',views.EXTLOGOUT,name="extlogout"),
        path('viewstructreport/',views.VIEWSTRUCTREPORT),
        path('processExtreport/',views.PROCESS_EXTREPORT),
        path('viewrequirement_ext/<int:id>/',views.VIEWREQUIREMENT_EXT),
        path('calcladding/<int:id>/',views.CALCLADDING),
        path('calstrawbale/<int:id>/',views.CALSTRAWBALE),
        path('viewextdata/<int:id>/',views.VIEWEXTDATAS),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
