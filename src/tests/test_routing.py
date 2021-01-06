import unittest

from flask import render_template
from src import app, routing

class Test_TestIncrementDecrement(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_increment(self):
        with self.app.test_request_context(): #with app.app_context(), app.test_request_context():
            self.assertEqual(routing.home(), render_template("home.html", name=None))

if __name__ == '__main__':
    unittest.main()
