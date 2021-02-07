import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app,create_app
from models import setup_db,Actor,Movie


casting_assistant = ("Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJzc1lHdmFOVzZsWG1zUVdiVXNZWXpqMlNzUHRYR2N6bEBjbGllbnRzIiwiYXVkIjoiQ2FzdGluZyIsImlhdCI6MTYxMjMwNDg5OSwiZXhwIjoxNjEyMzkxMjk5LCJhenAiOiJzc1lHdmFOVzZsWG1zUVdiVXNZWXpqMlNzUHRYR2N6bCIsInNjb3BlIjoiZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.eyGFHDLoPcvmR4Ci6AKR43JNT6lQDSp9M4mwK0Uv8sQsuHgqYAtu62OpURdA3q1hyyN82PpR8lZTie-4KjIkjgLf-pnUPk7TkpGZPHAVsHdilwUzqVeGBtJ451PathODScVoeXGvzGX1sMN5e7wUxeA7n8ZbV9RDUP0moM25VYaa9Qx5Fs8faCDxxri5m9hZJLGV03rqY2Kj36ktK5bs4Fq1fAUMMOAytnyFVy5VeUrQAH4Lnf52y3Px1_JcERyLpYHdLnrDhWSwEaRBbmBH2YB0MY-wAPf6UNH6Iyond-O1bDyjlr9Zqvfu6HDhFxSZIiAd2l8DodfW8h29jXhvFA")
executive_producer = ("Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJzc1lHdmFOVzZsWG1zUVdiVXNZWXpqMlNzUHRYR2N6bEBjbGllbnRzIiwiYXVkIjoiRXhlY3R1dGl2ZSBEaXJjZWN0b3IiLCJpYXQiOjE2MTIzMDUxNjcsImV4cCI6MTYxMjM5MTU2NywiYXpwIjoic3NZR3ZhTlc2bFhtc1FXYlVzWVl6ajJTc1B0WEdjemwiLCJzY29wZSI6InBvc3Q6bW92aWUgcG9zdCA6YWN0b3JzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBkZWxldGU6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicG9zdDptb3ZpZSIsInBvc3QgOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIl19.lYko9fbH11Qb1OTFl0Nyzas2SPEr6SXA28XbQd6ySkqsGWvUuuiY5XKHmbTJsOPfdI5XdLrRYCxy9P9qCQfMutnKfpxxhOvCt6p1QLeWndWXqkfqhDRu26RCASvptmE0t1qxmf-DWGiZ7-gxnrrbPDuo-ikccCaGeUk07mTuvEAEfhvMMcs4lIPgphMvI5J8MbhZTvds4b99ScfmmDeHdC_9A0BGce-0raqrJc2SqsPmDLC7CsJSJmNowL-Vg-IyseKTt177y8fb0U_FWx1NUtaWtKY6JRE3x0l3qgLbcWj70XNRrlORxXZZdI55EyRoNzW0f1V24m4m_SGGUuANtA")
casting_director = ("Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imw5Ni1FZzk2M3F6VzVRN0Y2VmdkSyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhbGFhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJzc1lHdmFOVzZsWG1zUVdiVXNZWXpqMlNzUHRYR2N6bEBjbGllbnRzIiwiYXVkIjoiY2FzdGluZyBkaXJlY3RvciIsImlhdCI6MTYxMjMwNTIzMiwiZXhwIjoxNjEyMzkxNjMyLCJhenAiOiJzc1lHdmFOVzZsWG1zUVdiVXNZWXpqMlNzUHRYR2N6bCIsInNjb3BlIjoiZGVsZXRlOmFjdG9ycyBwYXRjaDphY3RvcnMgcGF0Y2ggOiBtb3ZpZXMgcG9zdDphY3RvcnMgZ2V0OmFjdG9ycyBnZXQ6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoIDogbW92aWVzIiwicG9zdDphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.e8BdSYAAFhpUP0jPU9BpHJ_NtU3ozxCAwxrKHK5vR6NMgmyhDbBGY5nvcHZ_QGqNkyHeM6FSaZme29NeaKlDEZPz9MT5j8AdHLgno0sm-sJ5Ge4wo3j8Ow-O4nqn0WKgwVjFN3nq1jPOVwNQIh1_rOFdxnbceDxVbU3wOXgS2Lt0w6XGwY_2JZ2NO9eQEVtTdq846nn4J7JA3aD8YsfbtYO3Wc2LLEkYWk9lPkpvJmfQKnQdTvZTuB5w2DbBQpLK39p5vZl7ZQ5paHdCpzZrrIoIWXLy7V54VxZnPs8KmmX6AJT6aBLe3Z-TioGa3pgkhCylEId-MvATv5NFshZMQg")

class CastingTest(unittest.TestCase):
    '''Setup test suite for the routes'''
    def setup(self):
        '''setup application'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        selfup_db(self.app, self.database_path) 
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer",
            'Token': token}

        
        self.test_movie = {
            'title':'wonder',
            'release_data':'2021-01-01'
        }

    def tearDown(self):
        '''Executed after each test'''
        pass

    def test_create_new_actor(self):
        ''' Test post new actor'''
        response = self.client().get(
            '/actors',
            headers=casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actorid(self):
        response = self.client().get(
            '/actors/1', headers=casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'],'Mike')

    def test_404_get_actorid(self):
        response = self.client().get(
            '/actors/100',headers=casting_assistant
            )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['error'],404)
        self.assertEqual(data['message'],'resource not found')

    def test_post_actor(self):
        response = self.client().post(
            '/actors', json={'name':'miley','age':20,'gender':'female' },
                       headers =executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.data,201)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['actor']['name'],'miley')
        self.assertEqual(data['actor']['age'],20)
        self.assertEqual(data['actor']['gender'],'Female')


    def test_400_postactor(self):
        response = self.client().post(
            '/actors',json={},headers=executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['error'],400)
        self.assertEqual(data['message'],'bad request')

    def test_401_postactor_unauthorized(self):
        response = self.client().post(
            '/actors',json={'name':'Alexandra','age':25,'gender':'female'},
            headers=casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,401)
        self.assertEqual(data['code'],'unauthorized')
        self.assertEqual(data['description'],'Permission not found')

    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',json = {'name':'Mike','age':25,'gender':'Male'},
            headers=executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['actor']['name'],'Mike')
        self.assertEqual(data['actor']['age'],25)
        self.assertEqual(data['actor']['gender'],'Male')
    
    def test_401_patchactor_unauthorized(self):
        response = self.client().patch(
            '/actors/1', json={'name':'James','age':28,'gender':'Male'},
            headers={'Authorization': f'Bearer {casting_assistan}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,401)
        self.assertEqual(data['code'],'unauthorized')
        self.assertEqual(data['description'],'Permission not found')

    def test_404_patchactor(self):
        response = self.client().patch(
            '/actors/123',json={'name':'Jones','age':25,'gender':'Male'},
            headers=executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.data)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['error'],404)
        self.assertEqual(data['message'],'resource not found')

    def test_delete_actor(self):
        response = self.client().delete(
            '/actor/2',headers=executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,401)
        self.assertEqual(data['code'],'unauthorized')
        self.assertEqual(data['description'],'Permission not found')

    def test_404_delActor(self):
        response = self.client().delete(
            '/actors/1234',executive_producer
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'resource not found')
   
    def test_get_movies(self):
        response = self.client().get(
            '/movies',headers = casting_assistant
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])

    def test_get_movie(self):
        response = self.client().get(
            '/movies/1', headers=casting_assistant
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'],'her')

    def test_404_getmovies(self):
        response = self.client().get(
            '/movies/100',headers = casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'],'world')
        self.assertEqual(
            data['movie']['release_data'],
            'sun 2/2/2021'
        )
    def test_400_postmovie(self):
        response = self.client().post(
            '/movies',json={},headers= executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.data)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['error'],400)
        self.assertEqual(data['message'], 'bad request')

    def test_401_postmovie_unauthorized(self):
        response = self.client().post(
            '/movies',json=self.test_get_movie,headers= casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,401)
        self.assertEqual(data['code'],'unauthorized')
        self.assertEqual(data['description'],'permission not found')

    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',json={'title':'Saw','release_date':'2022/5/13'},
            headers =executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['movie'])
        self.assertEqual(data['movie']['title'],'saw')
        self.assertEqual(
            data['movie']['release_date'],
            'sun, 2/2/2021'
        )
    def test_400_patchmovie(self):
        response = self.client().patch(
            '/movies/1',json={},headers =executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['error'],400)
        self.assertEqual(data['message'],'bad request')

    def test_401_patchmovie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers= casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'],'permission not found')
    
    def test_404_patchmovie(self):
        response = self.client().patch(
            '/movies/123',
            json=self.test_movie,
            headers= executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers=executive_producer
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])
    
    def test_401_deletemovie(self):
        response = self.client().delete(
            '/movies/2',
            headers= casting_assistant
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'permission not found')

    def test_404_deletemovie(self):
        response = self.client().delete(
            '/movies/1234',
            headers = executive_producer
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    
if __name__ == "__main__":
    unittest.main()