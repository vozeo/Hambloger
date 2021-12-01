from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
import os
import sqlite3

# config flask
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# connect db
db = sqlite3.connect('heheblog.db', check_same_thread=False)
cdb = db.cursor()
print("Opened database heheblog.db successfully")



# constant
REG_KEY = "hehepig"
basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: "+basedir)






#======================================================================
# something about images
#======================================================================

IMG_ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg", "gif"])
DEFAULT_AVATAR = "/static/images/avatar_default.jpg"
WORK_NOT_FOUNT = "/static/images/work_not_found.png"

def img_allowed_file(filename, img_allowed_ext = IMG_ALLOWED_EXTENSIONS):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in img_allowed_ext


@app.route("/upload_image", methods=["GET", "POST"])
def upload_test():
    # Check login
    if not session.get("userid"):
        return render_template("error.html", message="Please login first.", link="/index")
    return render_template("upimg.html")


# upload a image
# userid:   session.userid (must login first)
# file:     image
# save as:  basedir/static/images/fname
# fname:    fname (default: fname=tmp)
@app.route("/api/upload_image", methods=["POST"])
def api_upload_image():

    # Check login
    userid = session.get("userid")
    if not userid:
        return render_template("error.html", message="Please login.", link="/login")

    # get ext
    file = request.files.get("image")
    ext=""
    if file and img_allowed_file(file.filename):
        ext = file.filename.rsplit('.',1)[1]

    # upload to database and generate the filename
    fname = request.form.get("fname")
    if len(fname) == 0:
        fname = "No Name"
    cdb.execute("INSERT INTO works (workname, authorid, ext) VALUES (?, ?, ?)",[fname, userid, ext])
    db.commit()
    cdb.fetchall()
    cdb.execute("SELECT LAST_INSERT_ROWID() FROM works")
    workid = cdb.fetchone()[0]
    filename = "work_workid" + "_" + str(workid)
    # upload imgfile to server
    if upload_image(file, filename):
        return redirect("/myspace")
    else:
        # if failed, delete the information from database
        cdb.execute("DELETE FROM works WHERE workid = ?", [workid])
        db.commit()
        return render_template("error.html", message="Failed.(Just accept jpg/jpeg/png/gif)", link="/myspace")


# file:     *.jpg | *.png
# save as:  bassdir/static/images/dir
# fname:    new_filename
# return 1 if succeeded, 0 if failed
def upload_image(file, new_filename):
    # Check login
    if not session.get("userid"):
        return render_template("error.html", message="Please login first.", link="/index")

    # direction
    file_dir = os.path.join(basedir, "static", "images")
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # filename and save
    if file and img_allowed_file(file.filename):
        fname = file.filename
        ext = fname.rsplit('.',1)[1]
        if not new_filename:
            new_filename="tmp"
        new_filename = new_filename + '.' + ext
        file.save(os.path.join(file_dir, new_filename))
        print("upload image ["+ os.path.join(file_dir, new_filename) + "] from user " + session.get("userid"))
        return True
    else:
        return False


# userid:       TEXT, 1~8 digits
# return an image url
def get_user_avatar(userid):
    if not userid:
        userid=""
    file_dir = "/static/images/avatar_userid_" + userid + ".jpg"
    if not os.path.isfile(basedir+file_dir):
        file_dir = DEFAULT_AVATAR
    return file_dir

def get_work_img(workid):
    if not workid:
        return WORK_NOT_FOUNT
    cdb.fetchall()
    cdb.execute("SELECT ext FROM works WHERE workid = ?", [workid])
    ext = cdb.fetchone()[0]
    file_dir = "/static/images/work_workid_" + str(workid) + "." + ext
    if not os.path.isfile(basedir+file_dir):
        file_dir = WORK_NOT_FOUNT
    return file_dir







#======================================================================
# basic usings
#======================================================================


def act_logout():
    session["userid"] = None
    session["avatar"] = DEFAULT_AVATAR

# index
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", get_user_avatar=get_user_avatar)


# login
@app.route("/login", methods=["GET","POST"])
def login():
    # Check current login status
    if session.get("userid") != None:
        return render_template("error.html", message="You are already logged in.", link="/")

    if request.method == "POST":

        # Verify
        # Check userid
        userid = request.form.get("userid")
        if not (userid.isdigit() and 0 < len(userid) < 9):
            return render_template("error.html", message="Invalid userid. (must be a 1~8 digits number)", link="/login")

        # Get real passwd
        cdb.execute("SELECT passwd FROM users WHERE userid = ?", [userid])
        row=cdb.fetchone()
        cdb.fetchall()
        if not row:
            return render_template("error.html", message="Userid doesn't exist. Click the link to see all users.", link="/userlist")
        real_passwd = row[0]

        # Check passwd
        input_passwd = request.form.get("passwd")
        if real_passwd != input_passwd:
            return render_template("error.html", message="Wrong passwd.", link="/login")

        # Remember that user logged in
        session["userid"] = userid
        session["avatar"] = get_user_avatar(userid)
        print("Change session[userid] to "+ userid)
        print("Change session[avatar] to "+ session["avatar"])

        # Redirect user to /
        return redirect("/")
    return render_template("login.html")


# logout
@app.route("/logout")
def logout():
    act_logout()
    return redirect("/")


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check key
        input_regkey = request.form.get("regkey")
        if input_regkey != REG_KEY:
            return render_template("error.html", message="Invalid Reg-key, please contact with hehepig.", link="/register")

        # Check userid
        userid = request.form.get("userid")
        if not (userid.isdigit() and 0 < len(userid) < 9):
            return render_template("error.html", message="Invalid userid. (must be a 1~8 digits number)", link="/register")
        cdb.fetchall()
        cdb.execute("SELECT COUNT(*) FROM users WHERE userid = ?", [userid])
        tmp = cdb.fetchone()[0]
        if tmp != 0:
            return render_template("error.html", message="This userid has already been used. Try another", link="/register")

        # Check passwd
        passwd = request.form.get("passwd")
        if len(passwd) == 0:
            return render_template("error.html", message="Invalid passwd. (can't be blank)", link="/register")

        # Generate default nickname
        nickname = "user_" + userid

        # Insert userdata into database
        cdb.execute("INSERT INTO users (userid, passwd, nickname) VALUES (?, ?, ?)", [userid, passwd, nickname])
        db.commit()


        # Redirect user to /login
        act_logout()
        return render_template("error.html", message="Successfully registered!", link="/login")
    return render_template("register.html")


# userlist
@app.route("/userlist")
def userlist():
    userlist = cdb.execute("SELECT userid, nickname FROM users")

    return render_template("userlist.html", userlist=userlist)

# userid
@app.route("/space", methods=["GET","POST"])
def space():

    # get userid
    if request.method == "POST":
        userid=request.form.get("userid")
    if request.method == "GET":
        userid=request.args.get("userid")

    # get worklist
    cdb.fetchall()
    cdb.execute("SELECT workid, workname FROM works WHERE authorid = ?", [userid])
    worklist = cdb.fetchall()

    # get nickname
    cdb.execute("SELECT nickname FROM users WHERE userid = ? LIMIT 1", [userid])
    nickname = cdb.fetchone()[0]

    # render template
    return render_template("myspace.html", nickname=nickname, userid=userid, worklist=worklist, get_work_img=get_work_img, get_user_avatar=get_user_avatar)


# myspace
@app.route("/myspace")
def myspace():
    # Check login
    if not session.get("userid"):
        return redirect("/login")
    return redirect("/space?userid="+session.get("userid"))









#======================================================================
# something about settings
#======================================================================


# settings
@app.route("/settings", methods=["GET","POST"])
def settings():
    # Check current login status
    userid = session.get("userid")
    if userid == None:
        return render_template("error.html", message="You are not logged in yet.", link="/logout")


    cdb.fetchall()
    cdb.execute("SELECT nickname FROM users WHERE userid = ?", [userid])
    userinfo = cdb.fetchall()[0]

    # Generate settings page
    return render_template("settings.html", userid=userid, nickname=userinfo[0], get_user_avatar=get_user_avatar)


@app.route("/settings/confirmavatar", methods=["POST"])
def confirm_settings_avatar():
    userid = session.get("userid")
    if not userid:
        return render_template("error.html")
    if request.method == "POST":
        print("user_"+userid+" is trying to change avatar")
        # Update avatar
        avatarfile=request.files.get("newimage")
        print("user_"+userid+"is trying to set new avatar: "+avatarfile.filename)
        if img_allowed_file(avatarfile.filename, ["jpg","png", "jpeg"]):
            avatarfile.filename = avatarfile.filename + ".jpg"
            upload_image(avatarfile,  "avatar_userid_"+userid)
    return redirect("/settings")
        


# confirm settings
@app.route("/settings/confirm", methods=["POST"])
def confirm_settings():
    if request.method == "POST":
        userid = session.get("userid")
        print("user_"+userid+" is trying to change settings")

        # Get Oldpasswd
        cdb.fetchall()
        cdb.execute("SELECT passwd FROM users WHERE userid = ?", [userid])
        real_oldpasswd = cdb.fetchone()[0]

        # Check Oldpasswd
        oldpasswd = request.form.get("oldpasswd")
        if (oldpasswd != real_oldpasswd):
            return render_template("error.html", message="Wrong Oldpasswd.", link="/settings")

        # Check Newpasswd
        newpasswd = request.form.get("newpasswd")
        confirmpasswd = request.form.get("confirmpasswd")
        if len(newpasswd) == 0:
            return render_template("error.html", message="Invalid passwd. (can't be blank)", link="/settings")
        if newpasswd != confirmpasswd:
            return render_template("error.html", message="Confirmpasswd is different from newpasswd", link="/settings")

        # Check Nickname
        nickname = request.form.get("nickname")
        if len(nickname) == 0:
            return render_template("error.html", message="Invalid nickname. (can't be blank)", link="/settings")


        # Update db
        cdb.execute("UPDATE users SET nickname = ?, passwd = ? WHERE userid = ?", [(nickname), (newpasswd), (userid)])
        db.commit()


        # Redirect user to /login
        act_logout()
        return render_template("error.html", message="Successfully changed your profile! Please relogin.", link="/login")
    return redirect("/settings")













#======================================================================
# something about follows
#======================================================================

def check_follow_exist(whofollow, followwho):
    cdb.fetchall()
    cdb.execute("SELECT COUNT(*) FROM follows WHERE whofollow = ? and followwho = ?", [whofollow, followwho])
    cnt = cdb.fetchone()[0]
    return (cnt != 0)

# if succeeded, return TRUE, otherwise return FALSE
def add_follow(whofollow, followwho):
    # Check weather the following relationship exists
    if check_follow_exist(whofollow, followwho) != 0:
        return False

    # If not exists, insert
    cdb.execute("INSERT INTO follows (whofollow, followwho) VALUES (?, ?)", [whofollow, followwho])
    db.commit()
    return True

# if succeeded, return TRUE, otherwise return FALSE
def del_follow(whofollow, followwho):
    # Check weather the following relationship exists
    if check_follow_exist(whofollow, followwho) == 0:
        return False

    # If exists, delete
    cdb.execute("DELETE FROM follows WHERE whofollow = ? and followwho = ?", [whofollow, followwho])
    db.commit()
    return True


# return userids that userid follows
def get_followlist(userid):
    cdb.fetchall()
    cdb.execute("SELECT followwho FROM follows WHERE whofollow = ?", [userid])
    return cdb.fetchall()


# returl:               return to returl
# whofollow, followwho: whofollow wants to follow followwho
@app.route("/follow", methods=["POST"])
def follow():
    if request.method == "POST":
        returl = request.form.get("returl")
        whofollow = request.form.get("whofollow")
        followwho = request.form.get("followwho")
        if not returl or not whofollow or not followwho:
            return render_template("error.html")
        whofollow = int(whofollow)
        followwho = int(followwho)
        print("%d wants to follow %d and redirect to %s" %(whofollow, followwho, returl))
        add_follow(whofollow, followwho)
    return redirect(returl)


# returl:               return to returl
# whofollow, followwho: whofollow wants to follow followwho
@app.route("/unfollow", methods=["POST"])
def unfollow():
    if request.method == "POST":
        returl = request.form.get("returl")
        whofollow = request.form.get("whofollow")
        followwho = request.form.get("followwho")
        if not returl or not whofollow or not followwho:
            return render_template("error.html")
        whofollow = int(whofollow)
        followwho = int(followwho)
        print("%d wants to unfollow %d and redirect to %s" %(whofollow, followwho, returl))
        del_follow(whofollow, followwho)
    return redirect(returl)



# userid
@app.route("/followlist")
def seefollowlist():
    if request.method == "GET":
        userid = request.args.get("userid")
    if not userid:
        return render_template("error.html")
    print(userid)
    followlist=get_followlist(userid)
    return render_template("followlist.html", userid=userid, followlist=followlist)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)