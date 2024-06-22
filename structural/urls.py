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
from structural import views

urlpatterns = [

        path('structure_login/',views.STRUCTURALLOGIN,name="structurallogin"),
        path('structural_reg/',views.STRUCTURALREG,name='structuralreg'),
        path('structhome/',views.STRUCTHOME,name='structhome'),
        path('struclogout/',views.STRUCLOGOUT,name="structlogout"),
        path('viewrequirement/',views.VIEWREQUIRE),
        path('viewclientdetails/<int:id>/',views.VIEWCLIENTDETAILS),
        path('processstruct/',views.PROCESSSTRUCT,name='processstruct'),
        path('calculatestructex/<int:id>/',views.CALCULATESTRUCTEX),
        path('calculatestructin/<int:id>/',views.CALCULATESTRUCTIN),
        path('calculatestructceil/<int:id>/',views.CALCULATESTRUCTCEIL),
        path('viewcalvalues/<int:id>/',views.VIEWCALVALUES),
        path('generatepdfstruct/<int:id>/',views.GENERATEPDFSTRUCT)

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
