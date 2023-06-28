from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Movie:
    db = 'movie_app'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genres = data['genres']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.reviewer = None


# crud method: Create
    @classmethod
    def save_movie(cls, data):
        query = """ 
        INSERT INTO movies 
        (title, genres, year, users_id)
        VALUES 
        (%(title)s, %(genres)s, %(year)s, %(users_id)s); """ 
        return connectToMySQL(cls.db).query_db(query, data)


# crud method: read
# combine get all users with get all movies = Movie.get_all()
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM movies
        LEFT JOIN users ON movies.users_id = users.id; """ 
        results = connectToMySQL(cls.db).query_db(query)

        all_movies = []

        for row in results:
            one_movie = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            one_movie.reviewer = user.User(user_data)

            all_movies.append(one_movie)

        return all_movies

# get one movie
# list in user will now have one movie
    @classmethod
    def get_one_movie(cls, data):
        query = """ SELECT * FROM movies
        LEFT JOIN users ON movies.users_id = users.idgenre
        WHERE movies.id = %(id)s; """ 

        results = connectToMySQL(cls.db).query_db(query, data)

        one_movie = cls(results[0])

        user_data = {
                'id': results[0]['users.id'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at'],
            }
        one_movie.reviewer = user.User(user_data)

        return one_movie


# update
    @classmethod
    def update_movie(cls, data):
        query = """ UPDATE movies
        SET title = %(title)s, genres = %(genres)s, year = %(year)s
        WHERE id = %(id)s; """ 

        return connectToMySQL(cls.db).query_db(query, data)


# delete
    @classmethod
    def delete_movie(cls, data):
        query = """ DELETE FROM movies
        WHERE id = %(id)s; """ 

        return connectToMySQL(cls.db).query_db(query, data)




# validation
    @staticmethod 
    def validate_movie(data):
        is_valid = True

# validate_title ->
        if len(data['title']) == 0:
            is_valid = False
            flash('title can not be left empty', 'movie')
# validate_genre ->
        if len(data['genres']) == 0:
            is_valid = False
            flash('genres can not be left empty', 'movie')
# validate_year ->
        if len(data['year']) == 0:
            is_valid = False
            flash('Year can not be left empty', 'movie')

        return is_valid