# db_tool/tests/test_database.py
import unittest
from db_tool.database import AsyncDatabaseConnection

class TestDatabaseConnection(unittest.TestCase):
    def test_mysql_connection(self):
        db = AsyncDatabaseConnection(db_type="mysql", user="root", password="password", host="localhost", database="test_db")
        db.connect()
        result = db.execute_query("SELECT 1")
        self.assertEqual(result, [(1,)])
        db.close()

if __name__ == '__main__':
    unittest.main()

