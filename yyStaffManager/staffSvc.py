from yyStaffManager.models import YYStaffInfo
import logging

logger = logging.getLogger('staffSvc')
def getStaffByID(pk):
    try:
        staffInfo = YYStaffInfo.objects.get(pk=pk)
        return staffInfo
    except YYStaffInfo.DoesNotExist:
        logger.warn('Failed to get the StaffInfo by ID: %d' % pk)
        return None
    return None
    