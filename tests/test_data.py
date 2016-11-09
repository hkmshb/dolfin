import os
import unittest
import openpyxl

from dolfin import Storage as _
from dolfin.data import XlSheet, TypedXlReaderBase



class StudentReader(TypedXlReaderBase):

    def _get_column_name_index_map(self):
        names = ('sn', 'name', 'gender', 'age')
        return _(zip(names, range(4)))

    def get_rows(self):
        headers, get = (('sn', 'name'), self._get_data)
        cols = self._get_column_name_index_map()
        self._ensure_headers_exists(headers)

        # iterate rows and extract students
        for row in self.xlsheet:
            student = _({
                'name': get(row, cols.name),
                'gender': get(row, cols.gender),
                'age': get(row, cols.age)
            })
            yield student


class XlSheetMixin:
    dir_base = os.path.dirname(__file__)

    def _get_xlsheet(self, sheet_name='students', row_offset=0):
        filepath = os.path.join(self.dir_base, 'fixtures', 'school.xlsx')
        xlsheet = XlSheet(filepath, sheet_name, row_offset=row_offset)
        return xlsheet
    

class XlSheetTestCase(unittest.TestCase, XlSheetMixin):

    def setUp(self):
        XlSheet.max_row_check = 10

    def test_can_be_created_using_workbook_filepath(self):
        xlsheet = self._get_xlsheet()
        self.assertIsNotNone(xlsheet)
    
    def test_cannot_create_from_non_existing_file(self):
        filepath = '/tmp/schools.xlsx'
        with self.assertRaises(OSError):
            XlSheet(filepath, 'students')

    def test_can_be_created_using_workbook_object(self):
        filepath = os.path.join(self.dir_base, 'fixtures', 'school.xlsx')
        workbook = openpyxl.load_workbook(filepath)
        xlsheet = XlSheet(workbook, 'students')
        self.assertIsNotNone(xlsheet)
    
    def test_cannot_create_from_non_Workbook_object(self):
        workbook = object()
        with self.assertRaises(ValueError):
            XlSheet(workbook, 'students')
    
    def test_can_iterate_rows_using_object(self):
        idx = 0
        for row in self._get_xlsheet():
            idx += 1
            self.assertIsNotNone(row)
        self.assertEqual(12, idx)
    
    def test_can_iterate_rows_using_next(self):
        xlsheet = self._get_xlsheet()
        idx, row = 0, xlsheet.next()
        try:
            while (row != None):
                idx += 1
                row = xlsheet.next()
        except:  # catches StopIteration exception throw at end of iteration
            pass
        self.assertEqual(12, idx)
    
    def test_can_iterate_rows_beginning_at_an_offset(self):
        idx = 1
        for row in self._get_xlsheet(row_offset=5):
            idx += 1
        self.assertEqual(8, idx)
    
    def test_can_combine_next_and_object_iteration_for_enumeration(self):
        xlsheet = self._get_xlsheet()
        for i in range(5):
            row = xlsheet.next()
        
        for r in xlsheet:
            i += 1
        self.assertEqual(11, i)
    
    def test_can_reset_iteration_halfway_using_row_offset_attribute(self):
        xlsheet = self._get_xlsheet()
        for i in range(7):
            row = xlsheet.next()
        self.assertEqual('sn', row[0])
        
        xlsheet.row_offset = 0
        for i in range(9):
            row = xlsheet.next()
        self.assertEqual(2, row[0])
        self.assertEqual('Jane Doe', row[1]) 
    
    def test_can_reset_iteration_calling_reset(self):
        xlsheet = self._get_xlsheet()
        for i in range(7):
            row = xlsheet.next()
        self.assertEqual('sn', row[0])
        
        xlsheet.reset()
        for i in range(9):
            row = xlsheet.next()
        self.assertEqual(2, row[0])
        self.assertEqual('Jane Doe', row[1])
    
    def test_can_find_headers_using_valid_samples(self):
        xlsheet = self._get_xlsheet()
        hdr_idx = XlSheet.find_headers(xlsheet, ['sn', 'name'])
        self.assertEqual(7, hdr_idx)
    
    def test_cant_find_headers_using_invalid_samples(self):
        xlsheet = self._get_xlsheet()
        hdr_idx = XlSheet.find_headers(xlsheet, ['sn', 'age'])
        self.assertEqual(-1, hdr_idx)
    
    def test_can_apply_offset_and_find_headers_using_valid_samples(self):
        xlsheet = self._get_xlsheet( )
        hdr_idx = XlSheet.find_headers(xlsheet, ['sn', 'name'], row_offset=4)
        self.assertEqual(7, hdr_idx)
    
    def test_can_limit_number_rows_checked_to_find_headers(self):
        xlsheet = self._get_xlsheet()
        XlSheet.max_row_check = 4
        hdr_idx = XlSheet.find_headers(xlsheet, ['sn', 'name'])
        self.assertEqual(-1, hdr_idx)


class TypedXlReaderTestCase(unittest.TestCase, XlSheetMixin):
    
    def setUp(self):
        XlSheet.max_row_check = 10

    def test_get_rows_returns_map_like_object(self):
        reader = StudentReader(self._get_xlsheet())
        for row in reader.get_rows():
            self.assertIsInstance(row, _)   # _=Storage
            self.assertIn("name", row)
            self.assertIn("gender", row)
            break

