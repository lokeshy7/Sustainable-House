from django.db import models

class exterior_details(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    poa= models.FileField(upload_to='media/')
    exteriorid= models.CharField(max_length=200, null=True)
    login = models.BooleanField(default=False, null=True)
    logout = models.BooleanField(default=True, null=True)
    appent = models.BooleanField(default=False, null=True)
