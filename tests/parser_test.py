import unittest
from blanketml.parser import parse


class TestParse(unittest.TestCase):

    def test_parse(self):
        res = parse(["co"])

        self.assertEqual(res, {"config_file": "co"})
