from django.db import models


class interior_details(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    poa= models.FileField(upload_to='media/')
    interiorid= models.CharField(max_length=200, null=True)
    login = models.BooleanField(default=False, null=True)
    logout = models.BooleanField(default=True, null=True)
    appint= models.BooleanField(default=False, null=True)
