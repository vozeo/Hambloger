from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField("Please enter your username: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


app = Flask(__name__)
app.config['SECRET_KEY'] = "Misaki is so handsome"
bootstrap = Bootstrap(app)

'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('你好像改变了自己的用户名')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template("index.html", form=form, name=session.get('name'))


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)
'''


@app.route("/editor")
def test():
    return render_template("editor.html")
