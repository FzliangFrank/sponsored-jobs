import unittest 
from drill.core import Job, Company


class TestJob(unittest.TestCase):
    def test_init(self):
        Job()

if __name__ == '__main__':
    unittest.main()