
'''
TODO: Add memory cache
'''
#class ErrorUtil:
    
#System error   
ERR_SYS_10001 = 10001



#Svc error

ERR_SVC_20000_USER_NOT_LOGON = 20000
ERR_SVC_20001 = 20001
ERR_SVC_20003_USER_NOT_EXIST = 20003
ERR_SVC_20004_CANT_FOCUS_SELF = 20004
ERR_SVC_20005 = 20005
ERR_SVC_20006_FORMAT_ERROR = 20006
ERR_SVC_20007_CANT_UNFOCUS_STRANGER= 20007
ERR_SVC_20008_UPLOAD_EMPTY_IMG = 20008
ERR_SVC_20009_UPLOAD_EXCEPTION = 20009
ERR_SVC_20010_UPLOAD_ALBUM_EXCEPTION = 20010
ERR_SVC_20011_STAFF_NOT_EXIST = 20011
ERR_SVC_20012_NO_AUTHORITY = 20012
ERR_SVC_20013_DB_EXCEPTION = 20013
ERR_SVC_20014_ALREADY_BIND_PHONE = 20014

    
ERR_DIC = {
           
   ERR_SYS_10001:"System error",
   ERR_SVC_20000_USER_NOT_LOGON:"User does not log on",
   ERR_SVC_20001:"Post<Get> Value error",
   ERR_SVC_20003_USER_NOT_EXIST:"User Not exist",
   ERR_SVC_20004_CANT_FOCUS_SELF:"User Can't focus him<her>self",
   
   ERR_SVC_20005:"Already Focus",
   
   ERR_SVC_20006_FORMAT_ERROR:"Format Error",
   ERR_SVC_20007_CANT_UNFOCUS_STRANGER:"Can't destroy friendship between stranger",
   ERR_SVC_20008_UPLOAD_EMPTY_IMG:"Upload empty image",
   ERR_SVC_20009_UPLOAD_EXCEPTION:"Upload Image exception",
   ERR_SVC_20010_UPLOAD_ALBUM_EXCEPTION:"Upload Album Exception",
   ERR_SVC_20011_STAFF_NOT_EXIST:"Staff Not exist",
   ERR_SVC_20012_NO_AUTHORITY:"No Authority",
   ERR_SVC_20013_DB_EXCEPTION:"DB Exception",
   ERR_SVC_20014_ALREADY_BIND_PHONE:"Already bind phone"
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