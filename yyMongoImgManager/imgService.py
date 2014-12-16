from yyMongoImgManager.models import YYImgInfo
import logging


logger = logging.getLogger("imgService")
def uploadImg(object):
    
    if object == None:
        logger.error('Upload empty image')
        raise Exception
    try:
        image = YYImgInfo()
        image.img = object
        image.width = image.img.width
        image.height = image.img.height
        image.save()
        return image.pk
    except:
        logger.error('Failed to upload image')
        return -1
    
def getImgUrl(iconID):
    return "/image/getImg?imageID="+iconID