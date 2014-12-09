from rest_framework import serializers
from yyTagManager.models import YYTagInfo
from rest_framework import pagination

class YYTagInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YYTagInfo
    
        fields = ('id','tagType','tagValue','status',
                  'createTime','updateTime','validTime')
        
class YYPaginatedTagInfoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = YYTagInfoSerializer