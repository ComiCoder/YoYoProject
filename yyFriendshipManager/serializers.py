from rest_framework import pagination
from rest_framework import serializers

from yyFriendshipManager.models import YYFriendShipInfo
from yyUserCenter.serializers import YYUserInfoSerializer


class YYFriendshipInfoSerializer(serializers.ModelSerializer):
    
    toUser = YYUserInfoSerializer()
    
    class Meta:
        model = YYFriendShipInfo
    
    
        fields = ('toUser','status',
                  'createTime','updateTime')