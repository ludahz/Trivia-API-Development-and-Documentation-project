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
        self.username = 'ludah'
        self.url = 'localhost:5432'
        self.database_path = 'postgresql://{}@{}/{}'.format(
            self.username, self.url, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertEqual(len(data["categories"]), 6)

    def test_get_question_search_with_results(self):
        res = self.client().post(
            "/questions", json={"searchTerm": "Africa?"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], 'Geography')
        self.assertTrue(data["total_questions"])
        self.assertEqual(len(data["questions"]), 1)

    def test_get_question_based_on_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], 'Science')
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

    """
    uncomment to test CREATE
    """

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json={
    #         "question": "Is this a test question",
    #         "answer": "Test answer",
    #         "category": 5,
    #         "difficulty": 5
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["created"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data['questions']))

    """
    uncomment to test DELETE
    """
    # def test_delete_question(self):
    #     res = self.client().delete("/questions/30")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["deleted"])
    #     self.assertTrue(len(data['questions']))

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
