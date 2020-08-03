from flask import Flask, render_template, flash, g, redirect, url_for, request
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from peewee import DoesNotExist

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'ailsdufalidhf9384029fbwdnfmsdff9238r'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None
    
    
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user
    
    
#@app.after_request
#def after_request():
#    g.db.close()
#    return response

@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(
                email=form.email.data,
                password=form.password.data
            )
        except ValueError:
            flash("User '{}' already exists.".format(form.email.data), "error")
        else:
            flash("User '{}' created successfully.".format(form.email.data), "success")
            return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except DoesNotExist:
            flash("Email or password does not match.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Email or password does not match.", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))


@app.route('/taco', methods=('GET', 'POST'))
@login_required
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(
            user=g.user._get_current_object(),
            protein=form.protein.data.lower(),
            shell=form.shell.data.lower(),
            cheese=form.cheese.data,
            extras=form.extras.data.lower()
        )
        flash("Taco created!", "success")
        return redirect(url_for('index'))
    elif request.method == 'POST':
        flash("Taco form is NOT valid, please try again.", "warning")
    return render_template('taco.html', form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='jamesanthenelli@aol.com',
            password='password'
        )
    except ValueError:
        pass
#        admin = models.User.get(models.User.email == 'jamesanthenelli@aol.com')
    app.run(debug=DEBUG, host=HOST, port=PORT)
    
        






