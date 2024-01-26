from django.db import models
import uuid

class pmp_user(models.Model):
    uuid = models.AutoField(primary_key=True)
    name = models.CharField("Enter Name",null=False)
    email = models.EmailField("Enter Email",null=False)
    phone = models.BigIntegerField("Enter Phone Number",null=False)

    class Meta:
        db_table = "pmp_users"
