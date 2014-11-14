from django.db import models
from yyUserCenter.models import YYAccountInfo
from yyImgManager.models import YYAlbumInfo
from YoYoProject import customSettings




# Create your models here.
class YYStaffInfo(models.Model):
    
    #STAFF_DEAL_TYPE CONSTANTS
    STAFF_DEAL_TYPE_TRADE = 1   #Trade
    STAFF_DEAL_TYPE_PRESENT = 2 #Present
    STAFF_DEAL_TYPE_SWITCH = 3  #Switch
    
    STAFF_DEAL_TYPE_CHOICES = (
                    (STAFF_DEAL_TYPE_TRADE,"Trade"),
                    (STAFF_DEAL_TYPE_PRESENT,"Present"),
                    (STAFF_DEAL_TYPE_SWITCH,"Switch"),
                    )
    
    
    dealType = models.SmallIntegerField(choices=STAFF_DEAL_TYPE_CHOICES,default=STAFF_DEAL_TYPE_TRADE)
    albumInfo = models.ForeignKey(YYAlbumInfo,null=True)
    staffDesc = models.CharField(max_length=300, null=True)
    price = models.FloatField(default=0.0)
    position = models.CharField(max_length=100, default='-')
    longitude = models.FloatField(default=0.0, null=True)
    latitude = models.FloatField(default=0.0, null=True)
    publisher = models.ForeignKey(YYAccountInfo, null=True)  #The Publisher Info
    status = models.SmallIntegerField(choices = customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    createTime = models.DateTimeField(auto_now_add=True, null=True)
    updateTime = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'yy_staff_info'
        
        


class YYPostInfo(models.Model):
    postUser = models.ForeignKey(YYAccountInfo, null=False)
    postStaff = models.ForeignKey(YYStaffInfo, null=False)
    description = models.CharField(max_length=300, null=True)
    status = models.SmallIntegerField(choices = customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    createTime = models.DateTimeField(auto_now_add=True, null=True)
    updateTime = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'yy_post_info'
        
    def getUserID(self):
        if self.postUser:
            return self.postUser.id
        else:
            return 0
        
        