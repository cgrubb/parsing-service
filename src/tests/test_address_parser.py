'''
Created on Mar 9, 2013

@author: cgrubb
'''
import unittest
from parsers import address_parser as ap


class Test(unittest.TestCase):
 
    def test_address_parser_simple(self):
        self.assertIsNotNone(ap.streetAddress)
        result = ap.streetAddress.parseString("3120 De la Cruz Boulevard")
        self.assertIsNotNone(result)
        self.assertEqual("3120", result.street.number.strip())
        self.assertEqual("De la Cruz", result.street.name)
        self.assertEqual("Boulevard", result.street.type)

    def test_address_parser_suite(self):
        result = ap.streetAddress.parseString("One Market, Suite 200")
        self.assertEqual("One", result.street.number.strip())
        self.assertEqual("Market", result.street.name)
        self.assertEqual("200", result.suite.suitenumber)
        
    def test_address_parser_intersection(self):
        result = ap.streetAddress.parseString("Bennet Rd & Main St")
        self.assertEqual("Bennet", result.crossStreet.name)
        self.assertEqual("Rd", result.crossStreet.type)
        self.assertEqual("Main", result.street.name)
        self.assertEqual("St", result.street.type)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()