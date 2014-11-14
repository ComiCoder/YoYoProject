from django.db import models
from YoYoProject import customSettings

# Create your models here.
class YYImageInfo(models.Model):
    
    IMG_UPLOAD_PATH = "images/normalImgs/"
    
    IMAGE_TYPE_STAFF = 1
    IMAGE_TYPE_ACTIVITY = 2
    
    IMAGE_TYPE_CHOICES = (
      (IMAGE_TYPE_STAFF,"Staff"),
      (IMAGE_TYPE_ACTIVITY,"Activity"),
    )
    
    imgURL = models.ImageField(upload_to=IMG_UPLOAD_PATH)
    width = models.SmallIntegerField()
    height = models.SmallIntegerField()
    type = models.SmallIntegerField(choices=IMAGE_TYPE_CHOICES,default=IMAGE_TYPE_STAFF)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'yy_image_info'
    
    
class YYAlbumInfo(models.Model):
    
    
    title = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=300,default='')
    status=models.SmallIntegerField(choices = customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    
    images = models.ManyToManyField(YYImageInfo, through='YYAlbum2Image')
    
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'yy_album_info'
    
    
class YYAlbum2Image(models.Model):
    
    
    albumInfo = models.ForeignKey(YYAlbumInfo)
    ImageInfo = models.ForeignKey(YYImageInfo)
    isPrimary = models.BooleanField(default="False")
    status=models.SmallIntegerField(choices = customSettings.INFO_STATUS_CHOICES, default=customSettings.INFO_STATUS_DEFAULT)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'yy_album_2_image'