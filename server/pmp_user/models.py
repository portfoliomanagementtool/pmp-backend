from django.db import models

# Create your models here.
class UserModel(models.Model):
    class Meta:
        db_table="users"
    uuid=models.TextField(primary_key=True)
    name=models.TextField()
    email=models.TextField()
    phone=models.BigIntegerField()