#!/usr/bin/env python

import unittest
from reader import checkClientKey

class TestCheckClientKey(unittest.TestCase):

    def setUp(self):
        clientKey = '123456789'

    def testNonEmptyKey(self):
        self.assertTrue( checkClientKey())

    def testEmptyStringKey(self):
        self.assertTrue( checkClientKey())


if __name__ == '__main__':
    unittest.main()
