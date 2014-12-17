WEIBO_ID_PREFIX = 'WEIBO_ID_'

USER_SESSION_KEY = 'USER_SESSION_KEY'

WEIBO_AUTH_TOKEN = 'WEIBO_AUTH_TOKEN'

GLOBAL_DESC_MAX_LENGTH = 300

INFO_STATUS_DELETE = 0
INFO_STATUS_DEFAULT = 1

INFO_STATUS_CHOICES = (
    (INFO_STATUS_DELETE,'delete'),
    (INFO_STATUS_DEFAULT,'default'),
)

INFO_DELETE_NO = 0
INFO_DELETE_YES = 1

INFO_DELETE_CHOICES = (
    (INFO_DELETE_NO,'default'),
    (INFO_DELETE_YES,'delete'),
)

USER_CERTIFICATION_TYPE_IDENTITY = 1
USER_CERTIFICATION_TYPE_WEIBO = 2
USER_CERTIFICATION_TYPE_WECHAT = 3

YOYO_MONGO_DB = 'yoyo_mongo_db'

GLOBAL_URL = 'http://localhost:8000'