from django.db import models
from YoYoProject import customSettings

# Create your models here.
class YYTagInfo(models.Model):
    TAG_TYPE_NORMAL = 1
    TAG_TYPE_OVERTIME = 2
    TAG_TYPE_CHOICES = (
                    (TAG_TYPE_NORMAL,"normal"),
                    (TAG_TYPE_OVERTIME,"overtime"),
                    )
    
    
    tagType = models.IntegerField(choices=TAG_TYPE_CHOICES, default=TAG_TYPE_NORMAL)
    tagValue = models.CharField(max_length=50,null=False)
    status = models.SmallIntegerField(choices=customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    createTime = models.DateTimeField(auto_now_add=True, null=True)
    updateTime = models.DateTimeField(auto_now=True, null=True)
    validTime = models.DateTimeField(null=True)