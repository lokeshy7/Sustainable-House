import random
import string

from django.contrib import messages
from django.shortcuts import redirect, render
from client.models import *



def BASEHOME(request):
    return render(request,'basehome.html')
def CLIENT_LOGIN(request):
    if request.method=="POST":
        email=request.POST['email']
        password = request.POST['password']
        try:
            d = client_details.objects.get(email=email, password=password)
            d.login = True
            d.logout = False
            d.save()
            messages.info(request, 'Logged in successfully ✅')
            return redirect('clienthome')
        except:
            messages.info(request,"Incorrect details ❌")
            return render(request, 'client_temp/client_log_reg.html')

    return render(request,'client_temp/client_log_reg.html')

def CLIENT_REG(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        currentsituation=request.POST['currentsituation']
        incomeproof=request.FILES['incomeproof']
        characters = string.ascii_letters + string.digits
        clientid = ''.join(random.choice(characters) for _ in range(9))
        try:

            client_details(name=name, email=email, password=password, phone=phone, currentsituation=currentsituation, incomeproof=incomeproof,
                          clientid=clientid).save()
            messages.info(request, "Client registered successfully ✅!")
            return redirect('clientlogin')
        except:
            print("33333333")
            messages.info(request, "Enter Valid data")
            return render(request, 'client_temp/client_register.html')
    return render(request, 'client_temp/client_register.html')

def CLIENT_HOME(request):
    return render(request,'client_temp/client_home.html')
def CLIENTLOGOUT(request):
    d=client_details.objects.get(login=True)
    d.login=False
    d.logout=True
    d.save()
    return redirect('basehome')

def UPLOADREQUIRE(request):
    # d = client_details.objects.get(login=True)
    # try:
    #     structuralrequirement.objects.get(clientid=d.clientid)
    #     messages.info(request,'Data Already uploaded')
    #     return redirect('clienthome')
    # except:
    return render(request,'client_temp/uploadrequire1.html')

def UPSTRUCTDET(request):
    d=client_details.objects.get(login=True)
    i=d.clientid
    if request.method=="POST":
        square=request.POST['square']
        rooms = request.POST['rooms']
        wall1width = request.POST['wall1width']
        wall2width = request.POST['wall2width']
        wall2height = request.POST['wall2height']
        wall1height = request.POST['wall1height']
        extthick = request.POST['extthick']
        intthick = request.POST['intthick']
        budget = request.POST['budget']
        roomwidth=request.POST['roomwidth']
        floorlen=request.POST['floorlen']
        floorwid=request.POST['floorwid']
        noofshelve=request.POST['noofshelve']
        try:
            structuralrequirement(square=square,rooms=rooms,wall1width=wall1width,wall2width=wall2width,wall2height=wall2height,
                                  wall1height=wall1height,extthick=extthick,intthick=intthick,budget=budget,clientid=i,roomwidth=roomwidth,floorwid=floorwid,
            floorlen=floorlen,noofshelve=noofshelve ).save()
            messages.info(request,'Uploaded successfully✔️')
            return redirect('clienthome')
        except:
            messages.info(request,"Enter valid data ❌")
            return render(request, 'client_temp/uploadrequire1.html')

    return redirect('clienthome')

def UPLOADINTREQUIREMENT(request):
    return render(request,'client_temp/uploadinterior.html')

def VIEWRESULT(request):
    d=client_details.objects.get(login=True)
    try:
        data=interiorrequire.objects.get(clientid=d.clientid)
        d2 = structuralrequirement.objects.filter(clientid=d.clientid)
        print('@@@@@@@@################@@@@@@@@@@@')
        return render(request, 'client_temp/viewresult.html', {'data': data, 'd2': d2, 'd': d})
    except:
        d2=structuralrequirement.objects.filter(clientid=d.clientid)
    return render(request,'client_temp/viewresult.html',{'d2':d2,'d':d})



