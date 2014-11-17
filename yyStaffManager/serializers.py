from rest_framework import serializers
from yyStaffManager.models import YYStaffInfo
from yyUserCenter.serializers import YYUserInfoSerializer
from rest_framework import pagination

class YYStaffInfoSerializer(serializers.ModelSerializer):
    
    publisher = YYUserInfoSerializer()
    
    class Meta:
        model = YYStaffInfo
    
        fields = ('dealType','albumInfo','staffDesc','price',
                  'position','longitude','latitude','publisher','status',
                  'createTime','updateTime')
        

class YYPaginatedStaffInfoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = YYStaffInfoSerializer