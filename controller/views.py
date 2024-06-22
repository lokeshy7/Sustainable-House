from django.contrib import messages
from django.shortcuts import redirect, render
from client.models import *
from structural.models import *
from exterior.models import *

from interior.models import *
def ADHOME(request):
    return render(request,'ad_temp/ad_home.html')
def ADMINLOG(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        predefined_email = 'admin@gmail.com'
        predefined_password = 'admin'

        if email == predefined_email and password == predefined_password:
            print('wqefefdd')
            messages.info(request,'Login successfully✔️')
            return redirect('adhome')
        else:
            messages.info(request,'Incorrect details ❌')
            return render(request,'ad_temp/adlog.html')
    return render(request,'ad_temp/adlog.html')

def ADLOGOUT(request):
    return redirect('basehome')
def SIAPPROVAL(request):
    d=structural_details.objects.all()
    return render(request,'ad_temp/siapproval.html',{'d':d})
def STRUCREPAPPROVAL(request):
    d=structuralrequirement.objects.all()
    return render(request,'ad_temp/structreportapprove.html',{'d':d})
def APPROVESTRUCTREP(request,id):
    d1=structuralrequirement.objects.get(id=id)
    d1.approve=True
    d1.save()
    d=structuralrequirement.objects.all()
    messages.info(request, 'Report approved successfully✔️')
    return render(request,'ad_temp/structreportapprove.html',{'d':d})

def EXTREPAPPROVE(request):
    d=structuralrequirement.objects.all()
    return render(request,'ad_temp/exterioreportapprove.html',{'d':d})

def APPROVEEXTREPORT(request,id):
    d1 = structuralrequirement.objects.get(id=id)
    d1.approveext = True
    d1.save()
    d = structuralrequirement.objects.all()
    messages.info(request, 'Report approved successfully✔️')
    return render(request, 'ad_temp/exterioreportapprove.html', {'d': d})

def VIEW_TOT_REP(request):
    d=interiorrequire.objects.all()
    return render(request, 'ad_temp/tot_rep_app.html',{'d':d})
def APPROVETOT_REP(request,id):
    d=interiorrequire.objects.get(id=id)
    i=d.clientid
    d2=structuralrequirement.objects.get(clientid=i)
    d2.incalculated=False
    d.approvetotrep=True
    d.save()
    d2.save()
    messages.info(request, 'Report approved successfully✔️')
    return redirect('viewtotrep')

def APPROVESTRUCT(request,id):
    d1 = structural_details.objects.get(id=id)
    d1.appstru=True
    d1.save()
    d = structural_details.objects.all()
    messages.info(request, 'Structural Integration approved successfully✔️')
    return render(request, 'ad_temp/siapproval.html', {'d': d})
def EA_APPROVAL(request):
    d = exterior_details.objects.all()

    return render(request, 'ad_temp/EA_approve.html', {'d': d})

def APPROVEENT(request,id):
    d1 = exterior_details.objects.get(id=id)
    d1.appent = True
    d1.save()
    d = exterior_details.objects.all()
    messages.info(request, 'Exterior acquisition approved successfully ✔️')
    return render(request, 'ad_temp/EA_approve.html', {'d': d})

def IIAPPROVAL(request):
    d = interior_details.objects.all()
    return render(request, 'ad_temp/II_approve.html', {'d': d})

def APPROVE_INT(request,id):
    d1 = interior_details.objects.get(id=id)
    d1.appint = True
    d1.save()
    d = interior_details.objects.all()
    messages.info(request, 'Interior Insulation approved ✔️')
    return render(request, 'ad_temp/II_approve.html', {'d': d})
