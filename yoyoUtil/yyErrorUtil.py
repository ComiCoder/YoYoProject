
'''
TODO: Add memory cache
'''
#class ErrorUtil:
    
#System error   
ERR_SYS_10001 = 10001



#Svc error

ERR_SVC_20000 = 20000
ERR_SVC_20001 = 20001
ERR_SVC_20003 = 20003
ERR_SVC_20004_CANT_FOCUS_SELF = 20004
ERR_SVC_20005 = 20005
ERR_SVC_20006_FORMAT_ERROR = 20006
ERR_SVC_20007_CANT_UNFOCUS_STRANGER= 20007
    
ERR_DIC = {
           
   ERR_SYS_10001:"System error",
   ERR_SVC_20000:"User does not log on",
   ERR_SVC_20001:"Post<Get> Value error",
   ERR_SVC_20003:"User does not exist",
   ERR_SVC_20004_CANT_FOCUS_SELF:"User Can't focus him<her>self",
   
   ERR_SVC_20005:"Already Focus",
   
   ERR_SVC_20006_FORMAT_ERROR:"Format Error",
   ERR_SVC_20007_CANT_UNFOCUS_STRANGER:"Can't destroy friendship between stranger"
           
}
    
    
def getErrorMsg(errorID):
    if ERR_DIC.has_key(errorID):
        return ERR_DIC.get(errorID)
    return "Not Defined Error"

def generateRsp(requestURL, errorID):
    
    rsp = {
        "requestURL":requestURL,
        "errorID":errorID,
        "errorMsg":getErrorMsg(errorID)
    }
    
    return rsp    