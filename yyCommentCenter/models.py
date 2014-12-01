from django.db import models
from mongoengine import connect
from mongoengine import Document
from YoYoProject import customSettings
from mongoengine.fields import IntField, StringField, DateTimeField


# Create your models here.
connect(customSettings.YOYO_MONGO_DB, host='127.0.0.1',port=27017)
class YYCommentInfo(Document):
    
    TARGET_TYPE_STAFF = 1
    TARGET_TYPE_DEAL = 2
    
    TARGET_TYPE_CHOICES = (
      (TARGET_TYPE_STAFF,"staff"),
      (TARGET_TYPE_DEAL,"deal"),
    )
    
   
    targetID = IntField(required=True)
    targetType = IntField(choices=TARGET_TYPE_CHOICES,default=TARGET_TYPE_STAFF)
    fromUserID = IntField(required=True)
    toUserID = IntField(required=False)
    comment = StringField(max_length=100)
    deleteStatus = IntField(choices=customSettings.INFO_DELETE_CHOICES, default=customSettings.INFO_DELETE_NO)
    createTime = DateTimeField()
    updateTime = DateTimeField()