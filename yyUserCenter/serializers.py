from rest_framework import serializers
from yyUserCenter.models import YYAccountInfo

class YYUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YYAccountInfo
        fields = ('phoneNum','nickName','iconID',
                  'gender','selfDesc','address','zipcode','email',
                  'type','regProvince','regCity',
                  'authValue','createTime','updateTime')