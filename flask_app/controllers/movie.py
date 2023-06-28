from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models import user, movie

@app.route('/movies/dashboard')
def list_movies():
    if 'uid' not in session:
        return redirect('/')
    data = {
        'id' : session['uid'],
    }
    return render_template("dashboard.html", one_user = user.User.get_user_by_id(data))


@app.route('/movies/new')
def new_movie():
    data = {
        'id' : session['uid'],
    }
    return render_template("new_movie.html", one_user = user.User.get_user_by_id(data))


@app.route('/movies/create', methods = ['POST'])
def create_movie():
    val_movie = movie.Movie.validate_movie(request.form)
    
    # if nothing is filled out in form, validation will acivate
    if not val_movie:
        return redirect('/movies/new')

    # if everything is filled out in form, takes user to dashboard
    one_movie = movie.Movie.save_movie(request.form)
    print(one_movie)
    return redirect('/movies/dashboard')
