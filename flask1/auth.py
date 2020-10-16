from flask import Blueprint,request,render_template,flash,g,abort,url_for,redirect,session,current_app
from flask1 import create_app,bcrypt_,db,login_manager
from flask_login import current_user,login_user,logout_user,login_required
from flask1.models import User
from flask1.forms import RegisterForm,Loginform

import functools
from markupsafe import escape


auth = Blueprint('auth',__name__)
app = create_app()

@current_app.before_request
def before_request():
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = User.query.get(user_id)


# def login_required(view):
#     @functools.wraps(view)
#     def wrapper(**kwargs):
#         if g.user == None:
#             print('this exe')
#             return redirect(url_for('auth.login'))
#         return view(**kwargs)
#     return wrapper

@auth.route('/register', methods = ('GET', 'POST'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt_.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data ,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} your account has been successfully created!')
        return redirect(url_for('auth.login'))
    return render_template('user/register.html',form = form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/login', methods = ('GET','POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.home_page'))

    # print(g.user)
    form = Loginform()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()

        if user and bcrypt_.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            login_user(user,remember= form.remember.data)
            flash('You have logged in successfully')
            next = request.args.get('next')
            if next:
                try:
                    return redirect(next)
                except:
                    return register(url_for('blog.home_page'))
            else:
                return redirect(url_for('blog.home_page'))
        else:
            flash('Wrong username or password')
    return render_template('user/login.html', form = form)



@auth.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
    session.clear()
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('auth.login'))