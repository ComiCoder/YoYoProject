from django.db import models

# Create your models here.
class errorInfo(models.Model):
    requestUrl = models.CharField(max_length=100)
    errorCode = models.SmallIntegerField()
    errorMsg = models.CharField(max_length=100)