from django.contrib.auth import authenticate, login
from yyUserCenter.models import YYAccountInfo
from YoYoProject.customSettings import USER_SESSION_KEY


def login(request, user):
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
    

class YYCustomBackend:
    
    def authenticate_by_id(self, user_id, password):
        try:
            user = YYAccountInfo.objects.get(pk=user_id)
        except YYAccountInfo.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None
    
    def authenticate(self, phoneNum=None, password=None):
        try:
            user = YYAccountInfo.objects.get(phoneNum=phoneNum)
        except YYAccountInfo.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None