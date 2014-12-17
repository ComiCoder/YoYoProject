# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from YoYoProject import customSettings
import yyMongoImgManager

# Create your models here.
class YYAccountInfo(models.Model):
     #GENDER Constants
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_NULL = 3
    GENDER_CHOICES = (
        (GENDER_MALE,'Male'),
        (GENDER_FEMALE,'Female'),
        (GENDER_NULL,'-')              
    )
    
    #UserType Constants
    USER_TYPE_NORMAL = 1
    USER_TYPE_ADMIN = 2
    
    USER_TYPE_CHOICES = (
        (USER_TYPE_NORMAL,'Normal'),
        (USER_TYPE_ADMIN,'Admin'),
    )
    
    REG_TYPE_PHONE = 1
    REG_TYPE_WEIBO = 2
    REG_TYPE_WEIXIN = 3
    
    ICON_UPLOAD_PATH = "images/profile_icon/"
    
    phoneNum = models.CharField(verbose_name="phone number", max_length=32, null=True)
    password = models.CharField(verbose_name="password", max_length=128, null=True)
    nickName = models.CharField(verbose_name="nick name", max_length=32, null=True)
    iconID = models.CharField(max_length=30, null=True)
    gender = models.SmallIntegerField(choices = GENDER_CHOICES, default=GENDER_NULL)
    selfDesc = models.CharField(max_length=300,null=True)
    address = models.CharField(max_length=128, null=True)
    zipcode = models.CharField(max_length=32, null=True)
    email = models.EmailField(null=True)
    type = models.SmallIntegerField(choices=USER_TYPE_CHOICES,default=USER_TYPE_NORMAL)
    regProvince = models.SmallIntegerField(null=True)
    regCity=models.SmallIntegerField(null=True)
    authValue = models.SmallIntegerField(default=0)
    
    authWeiboID = models.CharField(max_length=20, null=True) #sina weibo id
    deleteStatus = models.SmallIntegerField(choices=customSettings.INFO_DELETE_CHOICES, default=customSettings.INFO_DELETE_NO)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = 'pk'
    
    '''def is_admin(self):
        return self.type == self.USER_TYPE_ADMIN
    
    def check_password(self, password=None):
        if password == None:
            if self.password == None or len(self.password)==0:
                return True
        return self.password == password
        '''
    def getIconURL(self):
        if self.iconID:
            url = yyMongoImgManager.imgService.getImgUrl(self.iconID)
            print customSettings.GLOBAL_URL + url
            return customSettings.GLOBAL_URL + url
        return ""
    
    def getGender(self):
        if self.gender:
            if self.gender==YYAccountInfo.GENDER_MALE:
                return "男"
            elif self.gender==YYAccountInfo.GENDER_MALE:
                return "女"
        return "-"
        
    class Meta:
        db_table = 'yy_account_info'
        
        
class YYUserCertificationInfo(models.Model):
    
    STATUS_PENDDING = 1
    STATUS_DENIED = 2
    STATUS_APPROVED = 3
    
    STATUS_CHOICES = (
        (STATUS_PENDDING,'pending'),
        (STATUS_DENIED,'denied'),
        (STATUS_APPROVED,'approved'),
    )
    
    fromUser = models.ForeignKey(YYAccountInfo, null=False, related_name='fromUserID')
    identityImgID = models.CharField(max_length=30, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDDING)
    operationUser = models.ForeignKey(YYAccountInfo, null=True, related_name='operationUserID')
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    