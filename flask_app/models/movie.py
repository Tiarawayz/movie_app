from flask_app.config.mysqlconnection import connectToMySQL


class Movie:
  DB = 'movie_app'

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.title = data['title']
    self.genres = data['genres']
    self.year = data['year']
    self.created_at = data.get('created_at')
    self.updated_at = data.get('updated_at')

  @classmethod
  def save (cls, data):
    query = """INSERT into recipes (title, genres, year, user_id, created_at, updated_at) 
VALUES (%(user_id)s, %(title)s, %(genres)s, %(year)s, NOW(),NOW());"""
    results = connectToMySQL('movie_app').query_db(query, data)
    return results

  @classmethod
  def get_recipe_by_id(cls, id):
    query = """SELECT movies.id as id, title, genres, year, recipes.created_at, movies.updated_at, user_id, first_name AS posted_by FROM
    movies JOIN user ON user.id = movies.user_id WHERE movie.id = %(id)s;"""
    results = connectToMySQL('movie_app').query_db(query, {"id": id})
    return cls(results[0])

  @classmethod
  def get_all(cls):
    query = """SELECT movie.id as id, title, genres, year, movies.created_at, movies.updated_at, user_id, first_name AS posted_by FROM
    recipes JOIN user ON user.id = movies.user_id;"""
    results = connectToMySQL('movie_app').query_db(query)
    if not results:
      return []
    return [cls(row) for row in results]

  @classmethod
  def edit_recipe(cls, data):
    query = """UPDATE movie SET title=%(title)s, genres=%(genres)s, year=%(year)s, WHERE movie.id = %(id)s;"""
    results = connectToMySQL('movie_app').query_db(query, data)
    return results

  @classmethod
  def delete_recipe_by_id(cls, id):
    query = """DELETE FROM movies WHERE id = %(id)s;"""
    results = connectToMySQL('movie_app').query_db(query, {"id": id})
    return results

  @staticmethod
  def validate(data):
      errors = []

      required_fields = ('title', 'genres', 'year')
      for required_field in required_fields:
        if required_field not in data:
          errors.append(f"Missing required field '{required_field}'!")


      if len(data["name"]) < 2:
        errors.append("Name must contain atleast 2 characters.")

      if len(data["instructions"]) < 3:
        errors.append("Instructions must contain atleast 8 characters.")

      if len(data["description"]) < 3:
        errors.append("Description must contain atleast 8 characters.")

      is_valid = len(errors) == 0
      return is_valid, errors
