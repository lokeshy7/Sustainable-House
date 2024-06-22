import os
import random
import string
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from django.contrib import messages
from django.shortcuts import redirect, render
from structural.models import *
from client.models import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import joblib
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
def STRUCTURALLOGIN(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            structural_details.objects.get(email=email)
            try:
                structural_details.objects.get(email=email,password=password)
                try:
                    d = structural_details.objects.get(email=email, password=password,appstru=True)
                    d.login = True
                    d.logout = False
                    d.save()
                    messages.info(request, 'Logged in successfully ✅')
                    return redirect('structhome')
                except:
                    messages.info(request,'You need Controller approval')
                    return render(request, 'structural_temp/structural_logreg.html')
            except:
                messages.info(request, 'Enter correct password')
                return render(request, 'structural_temp/structural_logreg.html')

        except:
            messages.info(request, "Enter correct Mail id❌")
            return render(request, 'structural_temp/structural_logreg.html')
    return render(request,'structural_temp/structural_logreg.html')

def STRUCTURALREG(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        poa = request.FILES['poa']
        characters = string.ascii_letters + string.digits
        structid = ''.join(random.choice(characters) for _ in range(9))
        try:

            structural_details(name=name, email=email, password=password, phone=phone,
                           poa=poa,
                           structid=structid).save()
            messages.info(request, "Structural Integration registered successfully ✅!")
            return redirect('structurallogin')
        except:
            print("33333333")
            messages.info(request, "Enter Valid data")
            return render(request, 'structural_temp/structural_logreg.html')

    return render(request,'structural_temp/structural_logreg.html')
def STRUCTHOME(request):
    return render(request,'structural_temp/structhome.html')
def STRUCLOGOUT(request):
    d=structural_details.objects.get(login=True)
    d.login=False
    d.logout=True
    d.save()
    return redirect('basehome')

def VIEWREQUIRE(request):
    d1=structural_details.objects.get(login=True)
    d=structuralrequirement.objects.all()
    return render(request,'structural_temp/viewrequire.html',{'d':d})

def VIEWCLIENTDETAILS(request,id):
    d = structuralrequirement.objects.get(id=id)
    d1=client_details.objects.get(clientid=d.clientid)
    return render(request,'structural_temp/viewclientdetail.html',{'d1':d1})

def PROCESSSTRUCT(request):
    d = structuralrequirement.objects.all()
    return render(request,'structural_temp/processstruct.html',{'d':d})

def CALCULATESTRUCTEX(request,id):

        d1 = structuralrequirement.objects.get(id=id)
        height1 = d1.wall1height
        width1 = d1.wall1width
        ethickness = d1.extthick
        height2 = d1.wall2width
        width2 = d1.wall2height

        # Assuming you have a dataset with columns: 'wall_height', 'wall_width', 'ext_thickness', 'cebs_quantity', 'bamboo_beams', 'hempcrete_kg'
        # Load your dataset
        df = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\structure_dataset.csv')


        # Prepare features (X) and target variables (y)
        X = df[['Height', 'Width', 'Thickness']]
        y_cebs = df['Compressed Earth Blocks']
        y_bamboo = df['Bamboo']
        y_hempcrete = df['Hempcrete']

        # Split the data into training and testing sets
        X_train, X_test, y_cebs_train, y_cebs_test, y_bamboo_train, y_bamboo_test, y_hempcrete_train, y_hempcrete_test = train_test_split(
                X, y_cebs, y_bamboo, y_hempcrete, test_size=0.2, random_state=42
        )

        # Train the ANN models
        cebs_model = MLPRegressor(max_iter=1000)
        cebs_model.fit(X_train, y_cebs_train)

        bamboo_model = MLPRegressor(max_iter=1000)
        bamboo_model.fit(X_train, y_bamboo_train)

        hempcrete_model = MLPRegressor(max_iter=1000)
        hempcrete_model.fit(X_train, y_hempcrete_train)

        # Make predictions for a specific case
        new_data = {'wall_height': height1, 'wall_width': width1, 'ext_thickness': ethickness}
        cebs_quantity_pred = cebs_model.predict([list(new_data.values())])[0]
        bamboo_beams_pred = bamboo_model.predict([list(new_data.values())])[0]
        hempcrete_kg_pred = hempcrete_model.predict([list(new_data.values())])[0]
        new_data2 = {'wall_height': height2, 'wall_width': width2, 'ext_thickness': ethickness}
        cebs_wall2 = cebs_model.predict([list(new_data2.values())])[0]
        bamboo_wall2 = bamboo_model.predict([list(new_data2.values())])[0]
        hempcrete_wall2 = hempcrete_model.predict([list(new_data2.values())])[0]

        # Save the models for future use
        joblib.dump(cebs_model, 'cebs_model_ann.joblib')
        joblib.dump(bamboo_model, 'bamboo_model_ann.joblib')
        joblib.dump(hempcrete_model, 'hempcrete_model_ann.joblib')



        res = f"{cebs_quantity_pred} compressed earth blocks, {bamboo_beams_pred} bamboo beams, {hempcrete_kg_pred} kg hempcrete"
        print(res)
        d1=structuralrequirement.objects.get(id=id)
        d1.cebs_quantity_predex=round(cebs_quantity_pred,2)
        d1.bamboo_beams_predex=round(bamboo_beams_pred,2)
        d1.hempcrete_kg_predex=round(hempcrete_kg_pred,2)
        d1.cebs_wall2=round(cebs_wall2,2)
        d1.bamboo_wall2=round(bamboo_wall2,2)
        d1.hempcrete_wall2=round(hempcrete_wall2,2)
        d1.exwalcal=True
        d1.save()
        d = structuralrequirement.objects.all()
        return render(request, 'structural_temp/processstruct.html', {'d': d, 'res': res})


def CALCULATESTRUCTIN(request,id):
    d1 = structuralrequirement.objects.get(id=id)
    intthick=d1.intthick
    wall1height=d1.wall1height
    roomwidth=d1.roomwidth
    # Assuming you have a dataset with columns: 'wall_height', 'wall_width', 'ext_thickness', 'cebs_quantity', 'bamboo_beams', 'hempcrete_kg'
    # Load your dataset
    df = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\structure_dataset.csv')

    # Prepare features (X) and target variables (y)
    X = df[['Height', 'Width', 'Thickness']]
    y_cebs = df['Compressed Earth Blocks']
    y_bamboo = df['Bamboo']
    y_hempcrete = df['Hempcrete']

    # Split the data into training and testing sets
    X_train, X_test, y_cebs_train, y_cebs_test, y_bamboo_train, y_bamboo_test, y_hempcrete_train, y_hempcrete_test = train_test_split(
            X, y_cebs, y_bamboo, y_hempcrete, test_size=0.2, random_state=42
    )

    # Train the ANN models
    cebs_model = MLPRegressor(max_iter=1000)
    cebs_model.fit(X_train, y_cebs_train)

    bamboo_model = MLPRegressor(max_iter=1000)
    bamboo_model.fit(X_train, y_bamboo_train)

    hempcrete_model = MLPRegressor(max_iter=1000)
    hempcrete_model.fit(X_train, y_hempcrete_train)

    # Make predictions for a specific case
    new_data = {'wall_height': wall1height, 'wall_width': roomwidth, 'ext_thickness': intthick}
    cebs_quantity_predin = cebs_model.predict([list(new_data.values())])[0]
    bamboo_beams_predin = bamboo_model.predict([list(new_data.values())])[0]
    hempcrete_kg_predin = hempcrete_model.predict([list(new_data.values())])[0]
    d1.cebs_quantity_predin=round(cebs_quantity_predin,2)
    d1.bamboo_beams_predin=round(bamboo_beams_predin,2)
    d1.hempcrete_kg_predin=round(hempcrete_kg_predin,2)
    d1.inwalcal=True
    d1.save()
    d = structuralrequirement.objects.all()
    return render(request,'structural_temp/processstruct.html',{'d': d})
def CALCULATESTRUCTCEIL(request,id):
    d1 = structuralrequirement.objects.get(id=id)
    intthick=d1.intthick
    floorlen=d1.floorlen
    floorwid=d1.floorwid
    df = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\structure_dataset.csv')
    # Prepare features (X) and target variables (y)
    X = df[['Height', 'Width', 'Thickness']]
    y_cebs = df['Compressed Earth Blocks']
    y_bamboo = df['Bamboo']
    y_hempcrete = df['Hempcrete']
    # Split the data into training and testing sets
    X_train, X_test, y_cebs_train, y_cebs_test, y_bamboo_train, y_bamboo_test, y_hempcrete_train, y_hempcrete_test = train_test_split(
            X, y_cebs, y_bamboo, y_hempcrete, test_size=0.2, random_state=42)

    # Train the ANN models
    cebs_model = MLPRegressor(max_iter=1000)
    cebs_model.fit(X_train, y_cebs_train)

    bamboo_model = MLPRegressor(max_iter=1000)
    bamboo_model.fit(X_train, y_bamboo_train)

    hempcrete_model = MLPRegressor(max_iter=1000)
    hempcrete_model.fit(X_train, y_hempcrete_train)

    # Make predictions for a specific case
    new_data = {'wall_height': floorlen, 'wall_width': floorwid, 'ext_thickness': intthick}
    cebs_quantity_predceil = cebs_model.predict([list(new_data.values())])[0]
    bamboo_beams_predceil = bamboo_model.predict([list(new_data.values())])[0]
    hempcrete_kg_predceil = hempcrete_model.predict([list(new_data.values())])[0]
    d1.cebs_quantity_predceil=round(cebs_quantity_predceil,2)
    d1.bamboo_beams_predceil=round(bamboo_beams_predceil,2)
    d1.hempcrete_kg_predceil=round(hempcrete_kg_predceil,2)
    d1.cebs_quantity_predfloor = round(cebs_quantity_predceil,2)
    d1.bamboo_beams_predfloor = round(bamboo_beams_predceil,2)
    d1.hempcrete_kg_predfloor = round(hempcrete_kg_predceil,2)
    d1.ceilcal=True
    d1.save()
    d = structuralrequirement.objects.all()
    return render(request, 'structural_temp/processstruct.html', {'d': d})
def VIEWCALVALUES(request,id):
    d = structuralrequirement.objects.get(id=id)
    return render(request,'structural_temp/viewcal.html',{'d':d})

def GENERATEPDFSTRUCT(request,id):
        data = structuralrequirement.objects.get(id=id)

        # Create a title for the text file
        title = "STRUCTURAL INTEGRATION CALCULATED REPORTS"

        # Define the list data
        list_data = [
            f"CEBS Wall 1: {data.cebs_quantity_predex} kg",
            f"Bamboo Wall 1: {data.bamboo_beams_predex} g",
            f"Hempcrete Wall 1: {data.hempcrete_kg_predex} g/cm³",
            f"CEBS Wall 2: {data.cebs_wall2} meters",
            f"Bamboo Wall 2: {data.bamboo_wall2} meters",
            f"Hempcrete Wall 2: {data.hempcrete_wall2} g/cm³",
            f"CEBS Quantity Interior: {data.cebs_quantity_predin} kg",
            f"Bamboo Beams Interior: {data.bamboo_beams_predin} g",
            f"Hempcrete KG Interior: {data.hempcrete_kg_predin} g/cm³",
            f"CEBS Quantity floor: {data.cebs_quantity_predfloor} kg",
            f"Bamboo Beams floor: {data.bamboo_beams_predfloor} g",
            f"Hempcrete KG floor: {data.hempcrete_kg_predfloor} g/cm³",
            f"CEBS Quantity ceil: {data.cebs_quantity_predceil} kg",
            f"Bamboo Beams ceil: {data.bamboo_beams_predceil} g",
            f"Hempcrete KG ceil: {data.hempcrete_kg_predceil} g/cm³",
        ]

        # Concatenate the title and list data into a single string
        content = f"{title}\n\n" + '\n'.join(list_data)
        # Save the content as a file associated with the specific record
        file_content = ContentFile(content.encode('utf-8'))
        data.report.save(f"{title}_{data.id}.txt", file_content)
        data.structcalculate=True
        data.f=False
        data.save()
        messages.info(request,'Report Generated successfully✔️')
        return redirect('structhome')










