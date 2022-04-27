"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import model
import server
import crud

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies = []

for movie_dic in movie_data:
    date_str = movie_dic['release_date']


    format = "%Y-%m-%d"
    date = datetime.strptime(date_str, format)
    
    movie = crud.create_movie(movie_dic['title'], movie_dic['overview'], date, movie_dic['poster_path'])
    movies.append(movie)

model.db.session.add_all(movies)

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_movie = choice(movies)
        score = randint(1, 5)

        rating = model.Rating.create(user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()