from django.contrib.auth import authenticate, login

from YoYoProject.customSettings import USER_SESSION_KEY
from yyUserCenter.models import YYAccountInfo


def yyGetUserFromRequest(request):
    if yySessionHasKey(request):
        sessionUserID = request.session.get(USER_SESSION_KEY)
        user = YYAccountInfo.objects.get(pk = sessionUserID)
        if user:
            return user
    return None
        
def yyGetUserByID(userID):
    try:
        user = YYAccountInfo.objects.get(pk = userID)
        return user
    except YYAccountInfo.DoesNotExist:
        return None


def yySessionHasKey(request):
    sessionUserID = request.session.get(USER_SESSION_KEY)
    
    if sessionUserID == None:
        return False
    
    return True

def yyHasLogin(request, user):
    if USER_SESSION_KEY in request.session:
        userID = request.session[USER_SESSION_KEY]
        
        if userID == user.pk:
            return True
        else:
            return False
    else:
        return False
    
def yyIsWrongUser(request, user):
    if USER_SESSION_KEY in request.session:
        userID = request.session[USER_SESSION_KEY]
        if userID != user.pk:
            return True
    return False

def yyLogin(request, user):
    if user==None:
        return False
    
    if USER_SESSION_KEY in request.session:
        if request.session[USER_SESSION_KEY] != user.pk:
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
            return False
    else:
        request.session.cycle_key()
    request.session[USER_SESSION_KEY] = user.pk
    return True

def yyAuthenticateByID(user_id, password):
    try:
        user = YYAccountInfo.objects.get(pk=user_id)
    except YYAccountInfo.DoesNotExist:
        pass
    else:
        if user.check_password(password):
            return user
    return None

def yyGetUserByPhone(phoneNum):
    try:
        user = YYAccountInfo.objects.get(phoneNum=phoneNum)
        return user
    except YYAccountInfo.DoesNotExist:
        pass
    return None

def yyIsPasswordEquas(user, enterPwd):
    if user == None:
        return False
    
    if enterPwd==user.password:
        return True
    
    return False

    
    

class YYCustomBackend(object):
    '''
    def authenticate_by_id(self, user_id, password):
        try:
            user = YYAccountInfo.objects.get(pk=user_id)
        except YYAccountInfo.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None
    '''
    
    
    def authenticate(self, phoneNum=None, password=None):
        try:
            user = YYAccountInfo.objects.get(phoneNum=phoneNum)
        except YYAccountInfo.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None