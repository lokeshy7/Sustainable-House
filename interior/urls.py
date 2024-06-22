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
from interior import views

urlpatterns = [
path('interiorlogin/',views.INTERIORLOGIN,name="interiorlogin"),
        path('interiorregis/',views.INTERIORREGIS,name="interiorregis"),
        path('int_home/',views.INTHOME,name="inthome"),
        path('int_logout/',views.INTLOGOUT,name="intlogout"),
        path('viewinsrequire/',views.VIEWINSREQUIRE),
        path('process_shelve/',views.PROCESS_SHELVE),
        path('calc_shelve/<int:id>/',views.CALCSHELVE),
        path('process_flooring/',views.PROCESS_FLOOR),
        path('process_wallcover/',views.PROCESS_WALLCOVER),
        path('calwallcover/<int:id>/',views.CALWALLCOVER),
        path('calfloor/<int:id>/',views.CALFLOOR),
        path('view_intresults/',views.INTRESULTS),
        path('generatetotalreport/<int:id>/',views.GEN_TOT_REPORT)

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
