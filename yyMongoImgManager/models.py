from django.db import models
from mongoengine import Document
from mongoengine.fields import ImageField, IntField, DateTimeField
from mongoengine import connect

connect('yoyo_mongo_db', host='127.0.0.1',port=27017)
class YYImgInfo(Document):
    
    IMAGE_TYPE_PROFILE = 1
    IMAGE_TYPE_STAFF = 2
    IMAGE_TYPE_ACTIVITY = 3
    
    IMAGE_TYPE_CHOICES = (
      (IMAGE_TYPE_PROFILE,"Profile"),
      (IMAGE_TYPE_STAFF,"Staff"),
      (IMAGE_TYPE_ACTIVITY,"Activity"),
    )
    
    img = ImageField()
    width = IntField()
    height = IntField()
    type = IntField(choices=IMAGE_TYPE_CHOICES,default=IMAGE_TYPE_PROFILE)
    
    
