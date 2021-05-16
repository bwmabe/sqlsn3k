import shutil
import sqlite3

from unittest import TestCase

import sqlite_helpers


class TestModifiesDB(TestCase):
    def setUp(self):
        """
        Generates a list of queries that do or don't modify a database
        """
        self.queries = [("SELECT * FROM info ORDER BY lap_time ASC", False),
                        ("SELECT * FROM info WHERE class='Military'", False),
                        ("DROP TABLE t", True),
                        ("CREATE TABLE t", True),
                        ("INSERT INTO", True)]
        self.modifies_db = sqlite_helpers.modifies_db

    def test_modified(self):
        for query in self.queries:
            self.assertEqual(self.modifies_db(query[0]), query[1])
