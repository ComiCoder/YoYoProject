'''


@author: ryu
'''
from time import time

def generateFileName(id):
    fullName = str(time()).replace('.','_')+'_'+id
    return fullName
