'''


@author: ryu
'''
from time import time
import yyMongoImgManager

def generateFileName(id):
    fullName = str(time()).replace('.','_')+'_'+id
    return fullName

