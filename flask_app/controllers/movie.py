from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models.user import User
from flask_app.models.movie import Movie

@app.route('/dashboard')
def list_movies():

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    user = User.get_user_by_id(session["uid"])
    return render_template(
        "dashboard.html",
        current_user=user,
        recipes=Movie.get_all()
    )