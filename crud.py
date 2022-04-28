"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)    

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title = title, overview = overview, release_date = release_date, poster_path = poster_path)

    return movie

def get_movies():
    """Get all movies."""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """ Get movie by id. """

    return Movie.query.get(movie_id)

def get_users():
    """Get all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """ Get user by id. """

    return User.query.get(user_id)

def get_user_by_email(email):
    """ Get user by email. """

    return User.query.filter(User.email == email).first()



def create_rating(user_id, movie_id, score):
    """ Create and return a new rating """
    print (f" &&&&&& going to make a rating with user: {user_id} movie: {movie_id} score: {score}")

    rating = Rating(user_id = user_id, movie_id = movie_id, score = score)
    print (" ======== rating > ", rating)

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)