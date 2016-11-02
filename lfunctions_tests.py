import csv
import os
import unittest
import functions
import lfunctions
import pandas
import xlrd



@unittest.skipIf(functions.psycopg2_not_connected,"psycopg2 adapter not connected to the database atm and "
                                                  "it is necessary for the tests in this class")
class TestDBMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.cur = functions.psycodb95.cursor()

    def test_multiple_cursors_for_same_db_session(self):
        curB = functions.psycodb95.cursor()
        self.cur.execute('create temp table test0 as (select 0)')
        curB.execute('select * from test0')
        self.assertEquals(curB.fetchone()[0], 0)


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.auxf = lfunctions.AuxFCSV()

    def setUp(self):
        a = [{'a' : 1, 'b' : 8, 'c': 0}, {'a' : 2, 'b' : 33, 'c': 'zz'}]
        self.auxf.dicts_to_csv_ordrd(a, ['b','a','c'], 'test')
        self.auxf.dicts_to_csv_ordrd(a, ['a','b','c'], 'test1')

    def test_blank_fields(self):
        a = self.auxf.blank_fields(['', '    ', ' '])
        b = self.auxf.blank_fields([' a', '', ' b', '3'])
        self.assertTrue(a)
        self.assertFalse(b)

    def test_dict_list_to_csv_with_ordered_columns(self):
        with open('test.csv') as fh:
            dr = csv.reader(fh)
            self.assertEqual([row for row in dr][0], ['b','a','c'])

    def test_merge_csvs_with_column_order(self):
        self.auxf.merge_csvs_ordrd(['c', 'a', 'b'], 'test2', 'test.csv', 'test1.csv')
        with open('test2.csv') as fh:
            dr = csv.reader(fh)
            self.assertEqual([row for row in dr][0], ['c','a','b'])

    @classmethod
    def tearDownClass(self):
        os.remove('test.csv')
        os.remove('test1.csv')
        os.remove('test2.csv')


@unittest.skipIf(functions.psycopg2_not_connected, "psycopg2 adapter not connected to the database atm and "
                                                   "it is necessary for the tests in this class")
class TestPandasUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.eng = functions.psycodb95
        self.auxf = lfunctions.PdaUtils

    def setUp(self):
        df1 = pandas.read_sql_query('select timeofday();', self.eng)
        df2 = pandas.read_sql_query('select timeofday();', self.eng)
        self.dfs = [df1, df2]

    def test_data_frames_to_sheets_of_excel_spreadsheet(self):
        self.auxf.dframes_to_excel_sheets(self.dfs, ['time1', 'time2'], 'testdf')
        with pandas.ExcelFile('testdf.xlsx') as xls:
            df1 = pandas.read_excel(xls, 'time1')
            df2 = pandas.read_excel(xls, 'time2')
            self.assertTrue(not (df1.empty and df2.empty))

    @classmethod
    def tearDownClass(self):
        os.remove('testdf.xlsx')

