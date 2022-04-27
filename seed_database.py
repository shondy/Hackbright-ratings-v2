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
model.db.session.commit()