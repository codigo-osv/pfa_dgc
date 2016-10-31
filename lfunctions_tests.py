import csv
import os
import unittest
import functions
import lfunctions

class TestDBMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cur = functions.psycodb.cursor()

    def test_db_connection(self):
        self.assertEquals(functions.psycodb.closed, 0)

    def test_multiple_cursors_for_same_db_session(self):
        curB = functions.psycodb.cursor()
        self.cur.execute('create temp table test0 as (select 0)')
        curB.execute('select * from test0')
        self.assertEquals(curB.fetchone()[0], 0)


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.auxf = lfunctions.AuxFCSV()

    def test_blank_fields(self):
        a = self.auxf.blank_fields(['', '    ', ' '])
        b = self.auxf.blank_fields([' a', '', ' b', '3'])
        self.assertTrue(a)
        self.assertFalse(b)

    def test_dict_list_to_csv_with_ordered_columns(self):
        a = [{'a' : 1, 'b' : 8, 'c': 0}, {'a' : 2, 'b' : 33, 'c': 'zz'}]
        self.auxf.dicts_to_csv_ordrd(a, ['b','a','c'], 'test')
        with open('test.csv') as fh:
            dr = csv.reader(fh)
            self.assertEqual([row for row in dr][0], ['b','a','c'])

    @classmethod
    def tearDownClass(self):
        os.remove('test.csv')

