from django.db import models
from pmp_user.models import pmp_user
# Create your models here.


class Notification(models.Model):
    user= models.ForeignKey(pmp_user, on_delete=models.CASCADE,related_name='notification_user_id')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title