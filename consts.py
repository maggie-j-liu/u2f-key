HID_RPT_SIZE = 64  # Default size of raw HID report
CID_BROADCAST = 0xffffffff  # Broadcast channel id

TYPE_MASK = 0x80  # Frame type mask
TYPE_INIT = 0x80  # Initial frame identifier
TYPE_CONT = 0x00  # Continuation frame identifier

U2FHID_PING = (TYPE_INIT | 0x01)  # 129
U2FHID_MSG = (TYPE_INIT | 0x03)  # 131
U2FHID_LOCK = (TYPE_INIT | 0x04)  # 132
U2FHID_INIT = (TYPE_INIT | 0x06)  # 134
U2FHID_WINK = (TYPE_INIT | 0x08)  # 136
U2FHID_SYNC = (TYPE_INIT | 0x3c)  # 188
U2FHID_ERROR = (TYPE_INIT | 0x3f)  # 191

U2FHID_IF_VERSION = 2  # Current interface implementation version
CAPFLAG_WINK = 0x01  # Device supports WINK command
CAPFLAG_LOCK = 0x02  # Device supports LOCK command

U2F_REGISTER = 0x01
U2F_AUTHENTICATE = 0x02
U2F_VERSION = 0x03

ERR_NONE = 0x00
ERR_INVALID_CMD = 0x01
ERR_INVALID_PAR = 0x02
ERR_INVALID_LEN = 0x03
ERR_INVALID_SEQ = 0x04
ERR_MSG_TIMEOUT = 0x05
ERR_CHANNEL_BUSY = 0x06
ERR_LOCK_REQUIRED = 0x0a
ERR_SYNC_FAIL = 0x0b
ERR_OTHER = 0x7f
