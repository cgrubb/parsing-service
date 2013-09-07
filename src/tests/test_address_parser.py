'''
Created on Mar 9, 2013

@author: cgrubb
'''
import unittest
from parsers import address_parser as ap

tests = """\
    3120 De la Cruz Boulevard
    100 South Street
    123 Main
    221B Baker Street
    10 Downing St
    1600 Pennsylvania Ave
    33 1/2 W 42nd St.
    454 N 38 1/2
    21A Deer Run Drive
    256K Memory Lane
    12-1/2 Lincoln
    23N W Loop South
    23 N W Loop South
    25 Main St
    2500 14th St
    12 Bennet Pkwy
    Pearl St
    Bennet Rd and Main St
    19th St
    1500 Deer Creek Lane
    186 Avenue A
    2081 N Webb Rd
    2081 N. Webb Rd
    1515 West 22nd Street
    2029 Stierlin Court
    P.O. Box 33170
    The Landmark @ One Market, Suite 200
    One Market, Suite 200
    One Market
    One Union Square
    One Union Square, Apt 22-C""".split("\n")

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
    
    def test_address_parser_direction(self):
        result = ap.streetAddress.parseString("3120 N De la Cruz Boulevard")
        self.assertIsNotNone(result)
        self.assertEqual("N", result.street.prefix_direction)
        self.assertEqual("3120", result.street.number.strip())
        self.assertEqual("De la Cruz", result.street.name)
        self.assertEqual("Boulevard", result.street.type)

    def test_address_parser_weird_direction(self):
        result = ap.streetAddress.parseString("123 North South St")
        self.assertEqual("123", result.street.number.strip())
        self.assertEqual("North", result.street.prefix_direction)
        self.assertEqual("South", result.street.name)
        self.assertEqual("St", result.street.type)
    
    def test_address_parser_direction_suffix(self):
        result = ap.streetAddress.parseString("123 North South St N")
        self.assertEqual("North", result.street.prefix_direction)
        self.assertEqual("N", result.street.suffix_direction)
        self.assertEqual("South", result.street.name)
        self.assertEqual("St", result.street.type)
    
    def test_street_name_that_looks_like_prefix(self):        
        result = ap.streetAddress.parseString("123 N St N")
        self.assertEqual("123", result.street.number.strip())
        self.assertEqual("N", result.street.name)
    
    def test_whole_bunch_of_addresses(self):
        for address in tests:
            result = ap.streetAddress.parseString(address.strip())
            self.assertIsNotNone(result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()