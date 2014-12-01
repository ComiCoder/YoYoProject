from rest_framework import pagination
from rest_framework import serializers

from yyCommentCenter.models import YYCommentInfo
from yyStaffManager.models import YYStaffInfo, YYPostInfo
from yyUserCenter.serializers import YYUserInfoSerializer

import json


class YYCommentInfoSerializer(serializers.Serializer):
    targetID = serializers.CharField(max_length=64)
    targetType = serializers.IntegerField()
    fromUserID = serializers.CharField(max_length=64)
    toUserID = serializers.CharField(max_length=64)
    comment = serializers.CharField(max_length=300)
    createTime = serializers.DateTimeField()
    updateTime = serializers.DateTimeField()
    
    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.targetID = attrs.get('targetID', instance.targetID)
            instance.targetType = attrs.get('targetType', instance.targetType)
            instance.fromUserID = attrs.get('fromUserID', instance.fromUserID)
            instance.toUserID = attrs.get('toUserID', instance.toUserID)
            instance.comment = attrs.get('comment', instance.comment)
            instance.createTime = attrs.get('fromUserID', instance.createTime)
            instance.updateTime = attrs.get('fromUserID', instance.updateTime)
            return instance
        return YYCommentInfo(**attrs)
    
class YYPaginatedCommentInfoSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = YYCommentInfoSerializer
    
"""
class YYCommentInfoSerializer():
    def __init__(self, commentInfo):
        self.commentInfo = commentInfo
        
    def data(self):
        dict = {}
        dict['targetID'] = self.commentInfo.targetID
        dict['targetType'] = self.commentInfo.targetType
        dict['fromUserID'] = self.commentInfo.fromUserID
        dict['toUserID'] = self.commentInfo.toUserID
        dict['comment'] = self.commentInfo.comment
        #createTime = self.commentInfo.createTime
        
        #dict['createTime'] = self.commentInfo.createTime
        return json.dumps(dict)
        
    

class YYCommentInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = YYCommentInfo
    
        fields = ('targetID','targetType','fromUserID','toUserID',
                  'comment','createTime','updateTime')
        
""" 