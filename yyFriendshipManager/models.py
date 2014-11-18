from django.db import models
from yyUserCenter.models import YYAccountInfo
from YoYoProject import customSettings

# Create your models here.
class YYFriendShipInfo(models.Model):
    fromUser = models.ForeignKey(YYAccountInfo, null=False, related_name='fromUserID')
    toUser = models.ForeignKey(YYAccountInfo, null=False,related_name='toUserID')
    status = models.SmallIntegerField(choices = customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    createTime = models.DateTimeField(auto_now_add=True, null=True)
    updateTime = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'yy_friendship_info'