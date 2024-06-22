import random
import string

from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from interior.models import *
from client.models import *
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from django.shortcuts import render

def INTERIORLOGIN(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            interior_details.objects.get(email=email)
            try:
                interior_details.objects.get(email=email,password=password)
                try:
                    d = interior_details.objects.get(email=email, password=password,appint=True)
                    d.login = True
                    d.logout = False
                    d.save()
                    messages.info(request, 'Logged in successfully ✅')
                    return redirect('inthome')
                except:
                    messages.info(request, "You need admin approval")
                    return render(request, 'interior_temp/interior_log_reg.html')
            except:
                messages.info(request, "Enter correct Password")
                return render(request, 'interior_temp/interior_log_reg.html')

        except:
            messages.info(request, "Enter correct Mail id")
            return render(request,'interior_temp/interior_log_reg.html')
    return render(request,'interior_temp/interior_log_reg.html')

def INTERIORREGIS(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        poa = request.FILES['poa']
        characters = string.ascii_letters + string.digits
        interiorid = ''.join(random.choice(characters) for _ in range(10))
        interior_details(name=name, email=email, password=password, phone=phone,
                         poa=poa,
                         interiorid=interiorid).save()
        messages.info(request, "Interior Acquisition registered successfully ✅!")
        return redirect('interiorlogin')

    return render(request,'interior_temp/interior_log_reg.html')

def INTHOME(request):
    return render(request,'interior_temp/interior_home.html')

def INTLOGOUT(request):
    d = interior_details.objects.get(login=True)
    d.login = False
    d.logout = True
    d.save()

    return redirect('basehome')

def VIEWINSREQUIRE(request):
    d=structuralrequirement.objects.all()
    return render(request,'interior_temp/viewinsrequirement.html',{'d':d})

def PROCESS_SHELVE(request):
    d = structuralrequirement.objects.all()
    return render(request, 'interior_temp/processin_shelve.html', {'d': d})

def CALCSHELVE(request,id):
        d1 = structuralrequirement.objects.get(id=id)
        nos = d1.noofshelve
        if request.method == "POST":
            shelfheight = float(request.POST['shelfheight'])
            shelfwidth = float(request.POST['shelfwidth'])

        # Load your CSV file
        data = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\interior_temp\shelving2.csv')

        # Separate features and labels
        X = data[['Height', 'Width']]
        y = data[['bamboo height', 'bamboo width', 'quantityofbamboo']]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the decision tree regression model
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X_train, y_train)

        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Evaluate the model performance
        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')

        # Make predictions for new data
        new_data = [[shelfheight, shelfwidth]]
        predicted_bamboo_required = model.predict(new_data)
        print(predicted_bamboo_required[0])
        interiorrequire(clientid=d1.clientid,bambooheight=predicted_bamboo_required[0][0],bamboowidth=predicted_bamboo_required[0][1],
                        noofbamboo=predicted_bamboo_required[0][2]).save()
        d1.calshelve=True
        d1.save()

        print(f'Predicted Total Bamboo Required: {predicted_bamboo_required[0]}')

        # Continue with your Django code
        d = structuralrequirement.objects.all()
        return render(request, 'interior_temp/processin_shelve.html', {'d': d})


def PROCESS_FLOOR(request):
    d = structuralrequirement.objects.all()
    return render(request,'interior_temp/processin_floor.html',{'d': d})

def PROCESS_WALLCOVER(request):
    d = structuralrequirement.objects.all()
    return render(request, 'interior_temp/processin_wallcover.html', {'d': d})

def CALWALLCOVER(request,id):

    d1 = structuralrequirement.objects.get(id=id)
    d2 = interiorrequire.objects.get(clientid=d1.clientid)
    extwall1width=d1.wall1width
    extwall1height=d1.wall1height
    extwall2width = d1.wall2width
    extwall2height = d1.wall2height
    inwidht=d1.roomwidth
    nos = d1.noofshelve
    data = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\interior_temp\wall1.csv')
    X = data[['Height', 'Width']]
    y = data[['Total Wall Area']]
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    new_data = [[extwall1width, extwall1height]]
    extwall1cover = model.predict(new_data)
    new_data2 = [[extwall2width, extwall2height]]
    extwall2cover= model.predict(new_data2)
    new_data3 = [[inwidht, extwall1height]]
    intwallcover = model.predict(new_data3)
    d2.extwall1coverarea=extwall1cover
    d2.extwall1covercost=1500
    d2.extwall2coverarea=extwall2cover
    d2.extwall2covercost=1500
    d2.intwallcoverarea=intwallcover
    d2.intwallcovercost=1500
    d2.save()
    d1.calcover = True
    d1.save()
    # Continue with your Django code
    d = structuralrequirement.objects.all()
    return render(request, 'interior_temp/processin_wallcover.html', {'d': d})


def CALFLOOR(request,id):
    d = structuralrequirement.objects.all()
    return render(request, 'interior_temp/processin_floor.html', {'d': d})



def CALFLOOR(request, id):
    print("ersgzrf")
    d1 = structuralrequirement.objects.get(id=id)
    d2 = interiorrequire.objects.get(clientid=d1.clientid)
    floorlen=d1.floorlen
    floorwid=d1.floorwid
    nos = d1.noofshelve
    data = pd.read_csv(r'D:\PROJECT\SUSTAINABLE\sustainable_house\templates\interior_temp\floor2.csv')
    X = data[['Height', 'Width']]
    y = data[['Quantity of Linoleum (units)']]
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    new_data = [[floorlen, floorwid]]
    linoliumquantity = model.predict(new_data)
    d2.linoliumquantity = linoliumquantity
    d2.save()
    d1.calfloor = True
    d1.save()

    d = structuralrequirement.objects.all()
    return render(request, 'interior_temp/processin_floor.html', {'d': d})

def INTRESULTS(request):
    d=interiorrequire.objects.all()
    return render(request,'interior_temp/intresults.html',{'d':d})

def GEN_TOT_REPORT(request,id):
    d=interiorrequire.objects.get(id=id)
    i=d.clientid
    data=structuralrequirement.objects.get(clientid=i)
    # Create a title for the text file
    title = "TOTAL CALCULATED REPORTS"
    t="Structural Integration report"

    # Define the list data
    list_data = [
        f"CEBS Wall 1(per wall): {data.cebs_quantity_predex} kg",
        f"Bamboo Wall 1(per wall): {data.bamboo_beams_predex} g",
        f"Hempcrete Wall 1(per wall): {data.hempcrete_kg_predex} g/cm³",
        f"CEBS Wall 2(per wall): {data.cebs_wall2} meters",
        f"Bamboo Wall 2(per wall): {data.bamboo_wall2} meters",
        f"Hempcrete Wall 2(per wall): {data.hempcrete_wall2} g/cm³",
        f"CEBS Quantity Interior(per wall): {data.cebs_quantity_predin} kg",
        f"Bamboo Beams Interior(per wall): {data.bamboo_beams_predin} g",
        f"Hempcrete KG Interior(per wall): {data.hempcrete_kg_predin} g/cm³",
        f"CEBS Quantity floor: {data.cebs_quantity_predfloor} kg",
        f"Bamboo Beams floor: {data.bamboo_beams_predfloor} g",
        f"Hempcrete KG floor: {data.hempcrete_kg_predfloor} g/cm³",
        f"CEBS Quantity ceil: {data.cebs_quantity_predceil} kg",
        f"Bamboo Beams ceil: {data.bamboo_beams_predceil} g",
        f"Hempcrete KG ceil: {data.hempcrete_kg_predceil} g/cm³",
    ]

    title2="EXTERIOR ACQUISITION REPORTS"
    list_data2 = [
        f"Cork volume Wall 1(per wall): {data.corkvolumn_extwall1} m³",
        f"Cork volume Wall 2(per wall): {data.corkvolumn_extwall2} m³",
        f"Cork Size: {data.corksize} meters",
        f"No. of Straw Wall 1(per wall): {data.noofstraw1}",
        f"No. of Straw Wall 2(per wall): {data.noofstraw2}",
        f"Bale Size: {data.balesize} meters",
    ]

    title3 = "INTERIOR AND INSULATION REPORTS"
    list_data3 = [
        f"Bamboo Height(per shelve): {d.bambooheight} meters",
        f"Bamboo Width(per shelve): {d.bamboowidth} meters",
        f"Number Of Bamboo(per shelve): {d.noofbamboo}",
        f"Wall Cover Area(1)(per wall): {d.extwall1coverarea} square meters",
        f"Wall Cover Area(2)(per wall): {d.extwall2coverarea} square meters",
        f"Interior Wall Cover Area(per wall): {d.intwallcoverarea} square meters",
        f"Wall Cover Cost(Exterior1)(per wall): {d.extwall1covercost} cost unit",
        f"Wall Cover Cost(Exterior2)(per wall): {d.extwall2covercost} cost unit",
        f"Wall Cover Cost(Interior)(per wall): {d.intwallcovercost} cost unit",
        f"Linolium Quantity(flooring): {d.linoliumquantity} quantity unit",
    ]

    # Concatenate the title and list data into a single string
    content = f"{title}\n\n" +t+'\n'+ '\n'.join(list_data)+'\n\n'+f"{title2}\n\n" + '\n'.join(list_data2)+'\n\n'+f"{title3}\n\n" + '\n'.join(list_data3)
    # Save the content as a file associated with the specific record
    file_content = ContentFile(content.encode('utf-8'))
    d.totalreport.save(f"{title}_{data.id}.txt", file_content)
    d.genrep=True
    data.incalculated=True
    data.excalculated=False
    d.save()
    data.save()
    messages.info(request,'Report generated successfully ✅')
    return redirect('inthome')

