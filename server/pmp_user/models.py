from django.db import models
import uuid

class pmp_user(models.Model):
    uuid = models.AutoField(primary_key=True)
    name = models.CharField("Enter Name",null=True)
    email = models.EmailField("Enter Email",null=False)
    phone = models.BigIntegerField("Enter Phone Number",null=True)

    class Meta:
        db_table = "pmp_users"
