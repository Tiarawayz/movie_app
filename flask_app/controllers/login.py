from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_session import Session
from flask_app.models.user import User
from flask_app.models import user


Session(app)

@app.route('/')
def home():
    return render_template ('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    user = User.get_user_by_email(request.form["email"])
    if user is None or not User.verify_password(user, request.form["password"]):
        flash("Incorrect email or password!", "warning")
        return render_template("login.html")

    session["uid"] = user.id
    return redirect("/movies/dashboard")

@app.route('/user/register', methods={'POST'})
def register():
    is_valid, errors = User.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        return render_template("login.html")

    if request.form["password"] != request.form.get("password_confirmation"):
        flash("Password and password confirmation must be equal!", "error")
        return render_template("login.html")

    User.save({
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': User.hash_password(request.form['password']),
    })
    user = User.get_user_by_email(request.form["email"])
    flash('Thank you for registering')

    session["uid"] = user.id
    return redirect("/movies/dashboard")


@app.route('/logout')
def logout():
    session.pop("uid")
    return redirect("/")

#########

@app.route ('/users/profile/<int:id>')
def user_profile(id):
    if 'uid' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('profile.html',one_user=user.User.get_user_by_id(data))

@app.route('/users/edit/<int:id>')
def edit_user(id):
    if 'uid' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('update_user.html',one_user=user.User.get_user_by_id(data))

@app.route('/user/update', methods=['POST'])
def update_user():
    if 'uid' not in session:
        return redirect('/')
    if not user.User.is_valid_update(request.form):
        return redirect(f'/users/edit/{request.form["id"]}')
    user.User.update_user(request.form)
    return redirect('/movies/dashboard')


