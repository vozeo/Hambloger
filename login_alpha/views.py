
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from login_alpha import app, db, logm
from login_alpha.forms import LoginKey, LogoutKey, RegisterKey, LoginForm, RegisterForm
from login_alpha.extensions import load_user, idhash
from login_alpha.models import Users

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('nav'))

@app.route('/index.html', methods=['GET', 'POST'])
def nav():
    log_form = LoginKey()
    quit_form = LogoutKey()
    reg_form = RegisterKey()
    if request.method == 'POST':
        #if log_form.is_submitted():
        #    return redirect(url_for('login_main'))
        #elif reg_form.is_submitted():
        #    return redirect(url_for('reg_main'))
        #else:
        #    return redirect(url_for('nav'))
        if current_user.is_authenticated:
            if quit_form.submit3.data and quit_form.validate():
                logout_user()
                return redirect(url_for('nav'))
            elif reg_form.submit2.data and reg_form.validate():
                return redirect(url_for('reg_main'))
            else:
                return redirect(url_for('nav'))
        else:
            if log_form.submit1.data and log_form.validate_on_submit():
                print('bruh')
                return redirect(url_for('login_main'))
            elif reg_form.submit2.data and reg_form.validate_on_submit():
                return redirect(url_for('reg_main'))
            else:
                return redirect(url_for('nav'))
            
    else:
        if current_user.is_authenticated:
            p_title = 'Welcome, ' + current_user.nick
        else:
            p_title = 'Welcome, stranger!'
        return render_template('index.html', p_title=p_title, current_user=current_user, 
            lf=log_form, qf=quit_form, rf=reg_form)

@app.route('/login.html', methods=['GET', 'POST'])
def login_main():
    if current_user.is_authenticated:
        return redirect(url_for('nav'))

    form = LoginForm()
    if request.method == 'POST':
        if form.is_submitted():
            nick = form.nick.data
            pasw = form.key.data
            print('Login form submitted: %s %s' % (nick, pasw))
            user = Users.query.get(idhash(nick))
            if not form.validate():
                flash('Untrusted form post.', 'Alert')
                return redirect(url_for('login_main'))
            if user and user.validate_password(pasw):
                login_user(user)
                print('User login: %d' % (user.id))
                return redirect(url_for('nav'))
            else:
                flash('Invalid user or password.', 'Alert')
                return redirect(url_for('login_main'))
        else:
            flash('Invalid submission', 'Alert')
            return redirect(url_for('login_main'))
    else:
        return render_template('login.html', form=form)

@app.route('/register.html', methods=['GET', 'POST'])
def reg_main():
    form = RegisterForm()
    if request.method == 'POST':
        if form.is_submitted():
            nick = form.nick.data
            pasw = form.key.data
            pasw2 = form.keyc.data
            type = form.type.data
            # print('Register form submitted: %s %s %s %d' % (nick, pasw, pasw2, type))
            # 一些检查
            if not form.validate():
                flash('Untrusted submission.', 'Alert')
                return redirect(url_for('reg_main'))
            if pasw != pasw2:
                flash('Password not equal.', 'Alert')
                return redirect(url_for('reg_main'))
            if db.session.query(Users).get(idhash(nick)):
                flash('User existed!', 'Alert')
                return redirect(url_for('reg_main'))
            # 通过检查，添加新用户
            new_user = Users(
                id=idhash(nick),
                nick=nick, type=type
            )
            new_user.set_password(pasw)
            db.session.add(new_user)
            db.session.commit()
            # 弹成功消息，返回主页
            flash('Registration success.', 'Info')
            return redirect(url_for('nav'))
        else:
            print('Unauthorised submission')
            return redirect(url_for('reg_main'))
    else:
        return render_template('register.html', form=form)

@app.route('/demo')
def disp():
    users = db.session.query(Users).all()
    strlist = []
    length = len(users)
    print('DatabaseDebug: usercounter=%d' % (length))
    for i in users:
        print('DatabaseDebug: ' + str(i.__dict__))
        strlist.append(str(i.__dict__))
    return render_template('debug.html', list=strlist)
