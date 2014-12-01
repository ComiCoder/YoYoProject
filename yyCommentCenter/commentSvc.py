from yyCommentCenter.models import YYCommentInfo
import logging

logger = logging.getLogger(__name__)
def getCommentByID(pk):
    try:
        commentInfo = YYCommentInfo.objects.get(pk=pk)
        return commentInfo
    except YYCommentInfo.DoesNotExist:
        logger.warn('Failed to get the CommentInfo by ID: %d' % pk)
        return None
    return None