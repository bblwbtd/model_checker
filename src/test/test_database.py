import unittest

from src.database import *


class DatabaseCase(unittest.TestCase):
    def test_connection(self):
        db.create_tables(BaseModel.__subclasses__())


if __name__ == '__main__':
    unittest.main()
