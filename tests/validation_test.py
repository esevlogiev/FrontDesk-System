import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
from data_correctness import Validations


class ValidationTest(unittest.TestCase):
    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_validates_numbers(self):
        self.assertTrue(Validations.is_positive_integer('42'))
        self.assertFalse(Validations.is_positive_integer('42.5'))
        self.assertFalse(Validations.is_positive_integer('-42'))
        self.assertFalse(Validations.is_positive_integer('x'))
        self.assertTrue(Validations.is_float_number('42.42'))
        self.assertTrue(Validations.is_float_number('42'))
        self.assertFalse(Validations.is_float_number('x'))

    def test_validates_phone_numbers(self):
        self.assertTrue(Validations.is_phone('+35929555111'))
        self.assertTrue(Validations.is_phone('08812121212'))
        self.assertTrue(Validations.is_phone('+359 88 121-212-12'))
        self.assertFalse(Validations.is_phone('123123'))
        self.assertFalse(Validations.is_phone('+08812121212'))
        self.assertFalse(Validations.is_phone(' 08812121212'))
        self.assertFalse(Validations.is_phone('508812121212'))
        self.assertFalse(Validations.is_phone('a08812121212'))
        self.assertTrue(Validations.is_phone('008812121212'))
        self.assertFalse(Validations.is_phone('0008812121212'))
        self.assertFalse(Validations.is_phone('+08812121212 '))

    def test_validates_names(self):
        self.assertTrue(Validations.is_name('sdsd'))
        self.assertTrue(Validations.is_name('ASD'))
        self.assertTrue(Validations.is_name('vsaADFD'))
        self.assertFalse(Validations.is_name('svs2fdb'))
        self.assertFalse(Validations.is_name('svs fdb'))
        self.assertFalse(Validations.is_name('/fdb'))
        self.assertFalse(Validations.is_name(')2fdb'))
