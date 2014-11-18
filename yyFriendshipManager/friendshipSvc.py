from yyFriendshipManager.models import YYFriendShipInfo
def isFocusAlready(fromUserID, toUserID):
    q = YYFriendShipInfo.objects.filter(fromUser__pk =fromUserID, toUser__pk = toUserID)
    
    if q==None or q.count()==0:
        return False
    else:
        return True