import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:Live.absolutely1@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What player has won the most Super Bowls?',
            'answer': 'Tom Brady',
            'category': '6',
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):

        resp = self.client().get('/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])

    def test_404_request_invalid_page(self):
        
        resp = self.client().get('/questions?page=10000')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_question(self):
        resp = self.client().delete('/questions/6')
        data = json.loads(resp.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 6)
        self.assertEqual(question, None)

    def test_404_question_does_not_exist(self):
        resp = self.client().delete('/questions/10000')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_create_new_question(self):
        
        num_questions_before = len(Question.query.all())

        resp = self.client().post('/questions', json=self.new_question)
        data = json.loads(resp.data)

        num_questions_after = len(Question.query.all())

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(num_questions_after - num_questions_before == 1)

    def test_400_question_cannot_be_created(self):
        
        num_questions_before = len(Question.query.all())
        resp = self.client().post('/questions', json={})
        data = json.loads(resp.data)

        num_questions_after = len(Question.query.all())

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        self.assertTrue(num_questions_after == num_questions_before)

    def test_get_questions_by_category(self):

        resp = self.client().get('/categories/1/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_questions_by_category_fails(self):
        resp = self.client().get('/categories/100/questions')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_questions_search(self):
        resp = self.client().post('/questions/search', json={'searchTerm': 'human'})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_bad_search_term_results(self):
        resp = self.client().post('/questions/search', json={'searchTerm': 'adskfjasdfhasdpfad'})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_quiz_questions(self):
        resp = self.client().post('/quizzes', json={'previous_questions': [20],
                                                        'quiz_category': {'id': 1, 'type': 'Science'}})

        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)
        self.assertNotEqual(data['question']['id'], 3)

    
    def test_404_quiz_questions_fail(self):

        resp = self.client().post('/quizzes', json={})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()