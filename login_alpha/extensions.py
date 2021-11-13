
from login_alpha.models import Users
from login_alpha import db, logm

idhash_magic = 29
def idhash(name_str: str):
    global idhash_magic
    res = 0
    for char in name_str:
        res = res * idhash_magic + ord(char)
    return res % 998244353;

@logm.user_loader
def load_user(userid):
    print('load_user called: %s' % str(userid))
    try:
        user = Users.query.get(int(userid))
        return user
    except:
        return None