from flask import render_template
from . import main
from ..models import Post

@main.app_errorhandler(403)
def prohibition(e):
    edit_post = Post.query.order_by(Post.id.desc()).first()
    return render_template('403.html', edit_post=edit_post), 403


@main.app_errorhandler(404)
def page_not_found(e):
    edit_post = Post.query.order_by(Post.id.desc()).first()
    return render_template('404.html', edit_post=edit_post), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    edit_post = Post.query.order_by(Post.id.desc()).first()
    return render_template('500.html', edit_post=edit_post), 500
