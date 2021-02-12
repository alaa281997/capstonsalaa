# FSND: Capstone Project

## About 
 Capstone project for Udacity's Fullstack Nanodegree program. Summary : creating movies and managing and assigning actors.
 Herouku:https://alaacapstonproject.herokuapp.com/

 ## Getting starte 
 ### Key Dependencies
 -python 
 -Flask
 -Postgres
 -SQLAlchemy

 #### Installing Dependencies
 -python -m venv venv
 -source venv/Scripts/activate
 -pip install -r requirements.txt

##### Database Setup
 - export FLASK_APP=app
 - xport FLASK_DEBUG=Tru
 - flask run

#### Endpoints
GET /movies
{
  "movies": [
    {
      "id": 1,
      "date": "1-1-2021",
      "title": "Huch"
    },
    {
      "id": 2,
      "release_date": "1-1-2021",
      "title": "holidays"
    }
  ],
  "success": true
}

POST /movies

{
  "movie": {
    "id": 3,
    "release_date": "1-1-2021",
    "title": "lost"
  },
  "success": true
}
PATCH /movies/<int:id>
{
  "movie": {
    "id": 3,
    "release_date": "1-1-2021",
    "title": "lost"
  },
  "success": true
}
DELETE /movies/int:id\
{
  "message": "movie id 3, titled lost",
  "success": true
}
GET /actors
{
  "actors": [
    {
      "age": 20,
      "gender": "male",
      "id": 1,
      "name": "John"
    },
    {
      "age": 25,
      "gender": "male",
      "id": 2,
      "name": Mike"
    }
  ],
  "success": true
}
GET /actors/<int:id>
{
  "actor": {
    "age": 20,
    "gender": "male",
    "id": 1,
    "name": "John"
  },
  "success": true
}
POST /actors
General:
{
  "actor": {
    "age": 19,
    "gender": "female",
    "id": 3,
    "name": "Selena"
  },
  "success": true
}
PATCH /actors/<int:id>
General:
{
  "actor": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "Miley"
  },
  "success": true
}
DELETE /actors/int:id\
{
  "message": "actor id 3, named Miley was deleted",
  "success": true
}


#### Testing

- python -m unittest


#### Errors:
401 – unauthorized
404 – resource not found
405 - not allowed
422 – unprocessablet
