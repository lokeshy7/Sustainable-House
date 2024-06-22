import random
import string

from django.contrib import messages
from django.shortcuts import redirect, render
from exterior.models import *
from client.models import *
from sklearn.neural_network import MLPRegressor
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import joblib

def EXTERIORLOG(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            exterior_details.objects.get(email=email)
            try:
                exterior_details.objects.get(email=email,password=password)
                try:
                    d = exterior_details.objects.get(email=email, password=password,appent=True)
                    d.login = True
                    d.logout = False
                    d.save()
                    messages.info(request, 'Logged in successfully ✅')
                    return redirect('exteriorhome')
                except:
                    messages.info(request, "You need admin approval")
                    return render(request, 'exterior_temp/logreg.html')
            except:
                messages.info(request, "Enter correct password")
                return render(request, 'exterior_temp/logreg.html')

        except:
            messages.info(request, "Enter Correct Mail id")
            return render(request,'exterior_temp/logreg.html')

    return render(request,'exterior_temp/logreg.html')
def EXTERIORREG(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        poa = request.FILES['poa']
        characters = string.ascii_letters + string.digits
        exteriorid = ''.join(random.choice(characters) for _ in range(9))
        try:

            exterior_details(name=name, email=email, password=password, phone=phone,
                               poa=poa,
                               exteriorid=exteriorid).save()
            messages.info(request, "Exterior acquisition registered successfully ✅!")
            return redirect('exteriorlog')
        except:
            print("33333333")
            messages.info(request, "Enter Valid data")
            return render(request,'exterior_temp/logreg.html')
    return render(request,'exterior_temp/logreg.html')

def EXTERIORHOME(request):
    return render(request,'exterior_temp/exterior_home.html')

def EXTLOGOUT(request):
    d = exterior_details.objects.get(login=True)
    d.login = False
    d.logout = True
    d.save()
    return redirect('basehome')

def VIEWSTRUCTREPORT(request):
    d=structuralrequirement.objects.filter(approve=True)
    a=client_details.objects.all()
    return render(request,'exterior_temp/viewstructreport.html',{'d':d,'a':a})

def PROCESS_EXTREPORT(request):
    d = structuralrequirement.objects.filter(approve=True)
    return render(request,'exterior_temp/process_structreport.html',{'d':d})

def VIEWREQUIREMENT_EXT(request,id):
    d=structuralrequirement.objects.get(id=id)
    return render(request,'exterior_temp/viewrequirement_ext.html',{'d':d})

def CALCLADDING(request,id):
    d1 = structuralrequirement.objects.get(id=id)
    height1 = d1.wall1height
    width1 = d1.wall1width
    ethickness = d1.extthick
    height2 = d1.wall2width
    width2 = d1.wall2height

    # Assuming you have a dataset with columns: 'wall_height', 'wall_width', 'ext_thickness', 'cebs_quantity', 'bamboo_beams', 'hempcrete_kg'
    # Load your dataset
    df = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\cladding.csv')

    # Prepare features (X) and target variables (y)
    X = df[['Height', 'Width', 'Thickness']]
    y_thick = df['Cork Thickness']
    y_volume = df['Cork Volume']
    y_volumn_cu = df['Cork Volume (cu. yd)']

    # Split the data into training and testing sets
    X_train, X_test, y_thick_train, y_thick_test, y_volume_train, y_volume_test, y_volumn_cu_train, y_volumn_cu_test = train_test_split(
            X, y_thick, y_volume, y_volumn_cu, test_size=0.2, random_state=42
    )

    # Train the ANN models
    thick_model = MLPRegressor(max_iter=1000)
    thick_model.fit(X_train, y_thick_train)

    volumn_model = MLPRegressor(max_iter=1000)
    volumn_model.fit(X_train, y_volume_train)

    volumn_cu_model = MLPRegressor(max_iter=1000)
    volumn_cu_model.fit(X_train, y_volumn_cu_train)

    # Make predictions for a specific case
    new_data = {'wall_height': height1, 'wall_width': width1, 'ext_thickness': ethickness}
    corkvolumn_extwall1 = thick_model.predict([list(new_data.values())])[0]

    new_data2 = {'wall_height': height2, 'wall_width': width2, 'ext_thickness': ethickness}
    corkvolumn_extwall2 = thick_model.predict([list(new_data2.values())])[0]


    d1.corkvolumn_extwall1 = corkvolumn_extwall1

    d1.corkvolumn_extwall2 = corkvolumn_extwall2
    d1.corksize=0.5
    d1.calcork=True

    d1.save()
    d = structuralrequirement.objects.get(id=id)
    return render(request, 'exterior_temp/viewrequirement_ext.html', {'d': d})

def CALSTRAWBALE(request,id):
    d1 = structuralrequirement.objects.get(id=id)
    height1 = d1.wall1height
    width1 = d1.wall1width
    ethickness = d1.extthick
    height2 = d1.wall2width
    width2 = d1.wall2height

    # Assuming you have a dataset with columns: 'wall_height', 'wall_width', 'ext_thickness', 'cebs_quantity', 'bamboo_beams', 'hempcrete_kg'
    # Load your dataset
    df = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\strawbale.csv')
    print(df)

    # Prepare features (X) and target variables (y)
    X = df[['Height', 'Width', 'Thickness']]
    y_nob = df['NumberofBale']
    y_size = df['Wall Area']
    y_area_cu = df['Wall Area']

    # Split the data into training and testing sets
    X_train, X_test, y_nob_train, y_nob_test, y_size_train, y_size_test, y_area_cu_train, y_area_cu_test = train_test_split(
            X, y_nob, y_size, y_area_cu, test_size=0.2, random_state=42
    )

    # Train the ANN models
    nob_model = MLPRegressor(max_iter=1000)
    nob_model.fit(X_train, y_nob_train)

    size_model = MLPRegressor(max_iter=1000)
    size_model.fit(X_train, y_size_train)

    area_cu_model = MLPRegressor(max_iter=1000)
    area_cu_model.fit(X_train, y_area_cu_train)

    # Make predictions for a specific case
    new_data = {'wall_height': height1, 'wall_width': width1, 'ext_thickness': ethickness}
    noofstraw1 = nob_model.predict([list(new_data.values())])[0]

    new_data2 = {'wall_height': height2, 'wall_width': width2, 'ext_thickness': ethickness}
    noofstraw2 = nob_model.predict([list(new_data2.values())])[0]

    print(noofstraw1)
    d1.noofstraw1 = -(noofstraw1)

    d1.noofstraw2 = -(noofstraw2)
    d1.balesize='2.5 x 1.5 x 3'
    d1.corksize=0.5
    d1.calcork=True
    d1.calbale=True
    d1.save()
    d1.excalculated=True
    d1.structcalculate=False
    d1.save()
    d = structuralrequirement.objects.get(id=id)
    return render(request, 'exterior_temp/viewrequirement_ext.html', {'d': d})

def VIEWEXTDATAS(request,id):
    d=structuralrequirement.objects.get(id=id)
    return render(request,'exterior_temp/viewresults.html',{'d':d})