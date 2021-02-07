import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import  setup_db, Actor, Movie
from auth import AuthError, requires_auth, requires_signed_in

AUTH0_DOMAIN = "fsndalaa.us.auth0.com",
ALGORITHMS = ["RS256"],
API_AUDIENCE = "Casting",
AUTH0_CLIENT_ID ="ssYGvaNW6lXmsQWbUsYYzj2SsPtXGczl",
AUTH0_CALLBACK_URL="http://localhost:8080"



def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS')

        return response

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        ''' get actors '''
        actors = Actor.query.all()

        if actors is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor':actors.format()
                }), 200
    @app.route('/actors',methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
         '''post data'''
         data = request.get_json()
         name = data.get('name',None)
         age = data.get('age',None)
         gender = data.get('gender',None)

         actor = Actor(name = name, age = age , gender = gender)

         if name is None or age is None or gender is None:
           abort(400)

         try:
             actor.insert()
             return jsonify({
                 'success':True,
                 'actor':actor.format()
             }), 201
         except Exception:
            abort (500)

    @app.route('/actors/<actor_id>', methods = ['PATCH'])
    @requires_auth('edit:actors')
    def patch_actor(payload):
        ''' update an actor'''
        data = request.get_json()
        name = data.get('name',None)
        age = data.get('age',None)
        gender = data.get('gender',None)
 
        actor = Actor.query.get(actor_id)
    
        if actor is None:
           abort (404)
        if name is None or age is None or gender is None:
           abort(400)

        actor.name = name
        actor.age = age
        actor.gender = gender

        try:
          actor.update()
          return jsonify({
            'success':True,
            'actor': actor.format()
          }), 200
        except Exception:
            abort(500)
   
    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload):
     ''' Delete an actor'''
     actor = Actor.query.get(actor_id)

     if actor is None:
         abort (404)
     try:
         actor.delete()
         return jsonify({
             'success':True,
             'message':'Delete successfully'
         })
     except Exception:
         db.session.rollback()
         abort(500)

   
    @app.route('/movies/<movie_id>', methods = ['GET'])
    @requires_auth('get:movies')
    def get_movie(payload):
        ''' get movie '''
        
        movie = Movie.query.get(movie_id)
   
        if movie is None:
           abort (404)
        else:
          return jsonify({
              'success':True,
              'movie':movie.format()
           }), 200

    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
      ''' create movie'''
      data = request.get_json()
      title = data.get('title',None)
      release_date = data.get('release_data', None)

      if title is None or release_date is None:
          abort(400)
   
      movie = Movie(title = title , release_date = release_date)

      try:
           movie.insert()
           return jsonify({
              'success': True,
              'movie': movie.format()
           }),201
      except Exception:
          abort (500)

    @app.route('/movies/<movie_id>', methods = ['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(payload,movie_id):
        '''Update Movie'''
        data = request.get_json()
        title = data.get('title',None)
        release_date = data.get('release_date',None)

        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(404)
        if title is None or release_date is None:
            abort(400)

        movie.title = title
        movie.release_date = release_date

        try: 
            movie.update()
            return jsonify({
                'success':True,
                'movie': movie.format()
            }),200
        except Exception:
            abort (500)
    @app.route('/movies/<movie_id>', methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload):
        ''' delete a movie'''
        movie = Movie.query.get(movie_id)

        if movie is None:
            abort(400)
        try:
            movie.delete()
            return jsonify({
                'success':True,
                'message':'deleted successfully'
            })
        except Exception:
            db.session.rollback()
            abort(500)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success':False,
            'error':422,
            'message':'unprocessable'
        }),422
   
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'succcess': False,
            'error':400,
            'message':'bad request'
            }), 400
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success':False,
            'error':500,
            'message': 'internal server error'
        }), 500
    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            'success':False,
            'error':AuthError.status_code,
            'message':AuthError.error['description']
        }), AuthError.status_code


    return app

app = create_app()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)