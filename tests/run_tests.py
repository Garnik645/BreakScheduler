import os
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIRECTORY = os.path.join(ROOT_DIRECTORY, "src")
sys.path.append(SRC_DIRECTORY)

import unittest
from cls.domain import DomainConstructor
from cls.template import BreakInterval
from cls.template import BreakTemplateParser
from scheduler import parse_args

class TestSum(unittest.TestCase):

    def test_domain_validity(self):
        domain = (BreakInterval(1, 30), BreakInterval(40, 1000), BreakInterval(200, 300))
        result = DomainConstructor.is_domain_valid(domain)
        self.assertEqual(result, False, "Domain validity is wrong")
        
    def test_domain_dist(self):
        domain = (BreakInterval(1, 30), BreakInterval(40, 1000), BreakInterval(1020, 3000))
        result = DomainConstructor.min_break_dist(domain)
        self.assertEqual(result, 10, "Domain minimal distance is wrong")
        
    def test_parser(self):
        argv = [
            "--start-time", "10:10:10",
            "--end-time", "20:20:20",
            "--data-path", "",
            "--span-id", "2"]
        with self.assertRaises(FileNotFoundError):
            parse_args(argv)
            
    def test_time_parser(self):
        seconds = BreakTemplateParser.convert_time_to_seconds("10:10:10")
        self.assertEqual(seconds, 36610, "Time parser is wrong")
        
        
if __name__ == "__main__":
    unittest.main()