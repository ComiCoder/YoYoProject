from rest_framework import serializers
from yyTagManager.models import YYTagInfo

class YYTagInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YYTagInfo
    
        fields = ('pk','tagType','tagValue','status',
                  'createTime','updateTime','validTime')