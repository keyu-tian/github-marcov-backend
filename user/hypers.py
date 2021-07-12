import os
import re
from marcov19.settings import MEDIA_ROOT, SERVER_HOST, BASE_DIR



IDENTITY_CHS = (
    (1, 'root用户'),
    (2, '普通用户'),
    (3, '权威机构'),
)
VERCODE_CHS = (
    (1, '注册邮件'),
    (2, '找回密码')
)
# MESSAGE_type = (
#     (0, '其他'),
#     (1, '学者认证成功'),
#     (2, '学者认证被驳回'),
#     (3, '申诉学者成功'),
#     (4, '申诉学者被驳回'),
#     (5, '申诉学术成果成功'),
#     (6, '申诉学术成果被驳回'),
#     (7, '新增关注'),
#     (8, '新增学者认证申请'),
#     (9, '新增学术成果申诉'),
#     (10, '新增学者申诉'),
#     (11, '新增修改学术成果申请'),
#     (12, '申请修改学术成果成功'),
#     (13, '申请修改学术成果被驳回'),
# )
IDENTITY_DICT = {e[0]: e[1] for e in IDENTITY_CHS}
DEFAULT_AVATAR_ROOT = os.path.join(MEDIA_ROOT, 'avatar')          # 头像路径
MAX_UPLOADED_FSIZE = 10 * 1024 * 1024
FNAME_DEFAULT_LEN = 20

# constants
MINI_DATA_MAX_LEN = 32
BASIC_DATA_MAX_LEN = 96
EXT_DATA_MAX_LEN = 256
NAME_MAX_LEN = 16
PWD_MIN_LEN = 6
PWD_MAX_LEN = 16
DESC_MAX_LEN = 200
MAX_WRONG_PWD = 5

# checker lambdas
_TEL_REG = r'^[0-9]+$'
_EMAIL_REG = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
_PRINTABLE_UNICODES_WITHOUT_BLANK = lambda s: s.isprintable() and ' ' not in s
_PRINTABLE_ASCIIS_WITHOUT_BLANK = lambda s: _PRINTABLE_UNICODES_WITHOUT_BLANK(s) and all(ord(c) < 128 for c in s)

CHECK_NAME = lambda n: all([
    0 < len(n) <= NAME_MAX_LEN,
    _PRINTABLE_UNICODES_WITHOUT_BLANK(n),
])

CHECK_INTRO = lambda d: 0 <= len(d) <= 300

_CHECK_EMAIL = lambda e: all([
    0 < len(e) <= MINI_DATA_MAX_LEN,
    _PRINTABLE_ASCIIS_WITHOUT_BLANK(e),
    re.match(_EMAIL_REG, e),
])

_CHECK_TEL = lambda tel: all([
    0 < len(tel) <= MINI_DATA_MAX_LEN,
    all((c.isnumeric() or c == '+' or c == '-') for c in tel),
    re.match(_TEL_REG, tel),
])

CHECK_ACC = lambda acc: _CHECK_EMAIL(acc)

CHECK_AVATAR = lambda avatar: os.path.exists(BASE_DIR + re.findall(f'(?<=http://{SERVER_HOST}).*$', avatar)[0])
# 不清楚为何os.path.join不起作用

CHECK_PWD = lambda pwd: all([
    PWD_MIN_LEN <= len(pwd) <= PWD_MAX_LEN,
    _PRINTABLE_ASCIIS_WITHOUT_BLANK(pwd),
    any(c.isupper() for c in pwd)
    + any(c.islower() for c in pwd)
    + any(c.isnumeric() for c in pwd)
    + any(not c.isalnum() for c in pwd)
    >= 2
])

CHECK_DESCS = lambda d: 0 <= len(d) <= DESC_MAX_LEN
