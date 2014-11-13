from django.db import models
from django.contrib.auth.models import User

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
    smallIconURL = models.ImageField(upload_to=ICON_UPLOAD_PATH, null=True)
    largeIconURL = models.ImageField(upload_to=ICON_UPLOAD_PATH, null=True)
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
    
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    def is_admin(self):
        return self.type == self.USER_TYPE_ADMIN
    
    def check_password(self, password=None):
        if password == None:
            if self.password == None or len(self.password)==0:
                return True
        return self.password == password
    
    class Meta:
        db_table = 'yy-account_info'
    
    