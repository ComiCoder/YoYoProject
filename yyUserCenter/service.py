from YoYoProject import customSettings
import logging
from yyError.yyError import yyError

logger = logging.getLogger(__name__)

class UserService():
    def __certificateIdentity(self, userID, file):
        if userID == None:
            logger.error("Can't certificate User, the UserID is None")
            raise yyError(yyError.ERROR_ID_PARAMETER_EMPTY, "Need UserID parameter")
        if file == None:
            logger.error("Can't certificate User, the File is None")
            raise yyError(yyError.ERROR_ID_PARAMETER_EMPTY, "Need File parameter")
        
        pass
    
    def certificateUser(self, type, userID, otherID=None, file=None):
        if type == customSettings.USER_CERTIFICATION_TYPE_IDENTITY:
            return self.__certificateIdentity(userID, file)
        else:
            pass