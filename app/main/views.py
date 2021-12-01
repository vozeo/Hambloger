from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, NameForm, PostForm
from .. import db
from ..models import Permission, User, Post

#@main.route('/', methods=['GET', 'POST'])
#def index():
#    form = NameForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.name.data).first() #查询是否存在用户
#        if user is None: #若不存在用户
#            user = User(username=form.name.data)
#            db.session.add(user)
#            db.session.commit()
#            session['known'] = False
#        else:
#            session['known'] = True
#        old_name = session.get('name') #检测用户名是否发生变化
#        if old_name is not None and old_name != form.name.data:
#            flash('你好像改变了自己的用户名')
#        session['name'] = form.name.data
#        form.name.data = ''
#        return redirect(url_for('.index'))
#    return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('你的个人资料已更新')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)
