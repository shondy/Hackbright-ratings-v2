"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<movie_id>', methods = ["POST"])
def rate_movie(movie_id):
    """ Rate a specific movie """

    user_id = session["primary_key"]
    movie = crud.get_movie_by_id(movie_id)
    score = int(request.form.get("ratings"))
    print (f" ***** user: {user_id}  movie_id: {movie_id}")


    print(f" $$$$$ User { user_id } is rating movie: {movie} with score: {score}")
    new_rating = crud.create_rating(user_id, movie_id, score)
    print (" >>>>> our new rating is: ", new_rating)
    db.session.add(new_rating)
    db.session.commit()


    return render_template("movie_details.html", movie=movie)


@app.route('/movies/<movie_id>')
def display_movie(movie_id):
    """ Display info about specific movie """

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def display_user(user_id):
    """ Display info about specific user """

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route('/users', methods = ["POST"])
def create_user():
    """ Create a user from form data """

    email = request.form.get("email")
    password = request.form.get("password")
    temp_user = crud.get_user_by_email(email)

    if temp_user:
        flash("An account with that email already exists, please try again")
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Account created for user: {email}")

    return redirect("/")

@app.route('/login', methods = ["POST"])
def login():
    """ Log in a user to the app"""

    email = request.form.get("email")
    password = request.form.get("password")
    temp_user = crud.get_user_by_email(email)

    if temp_user:
        if temp_user.password == password:
            session["primary_key"] = temp_user.user_id
            flash("Logged in!")
        else: 
            flash("Wrong password, please, try again")
    else:
        flash(f"There is no user with email {email}")

    return redirect("/")




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
