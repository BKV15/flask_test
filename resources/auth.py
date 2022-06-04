from flask import Blueprint , request , redirect , render_template , url_for , flash
from werkzeug.security import generate_password_hash , check_password_hash
from .models import User
from flask_login import login_user , logout_user , current_user , login_required

auth = Blueprint('auth' , __name__)

@auth.route('/' , methods=('POST',))
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.objects(email=email).first()

    if user:
        if check_password_hash(user.password , password):
            login_user(user, remember=True)
            flash('Logged in successfully' , category='success')
            return redirect(url_for('views.ner'))
        else:
            flash('Password is incorrect' , category='error')
    else:
        flash('Account does not exist' , category='error')
    
    return redirect(url_for('views.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@auth.route('/sign-up' , methods=('GET' , 'POST'))
def sign_up():

    if request.method == 'POST':

        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.objects(email=email).first()

        if user:
            flash('Account already exist' , category='error')
        elif len(name) < 1:
            flash('Name filed is empty' , category='error')
        elif len(email) < 7:
            flash('Email is incorrect' , category='error')
        elif len(password1) < 4:
            flash('Password should be at least 4 characters' , category='error')
        elif password1 != password2:
            flash('Passwords don\'t match' , category='error')
        else:
            new_user = User(email=email,name=name,password=generate_password_hash(password1))
            new_user.save()
            flash('Account created' , category='success')
            return redirect(url_for('views.index'))

    if current_user.is_authenticated:
        flash('You are already logged in' , category='error')
        return redirect(url_for('views.ner'))
        
    return render_template('sign-up.html' , user=current_user)