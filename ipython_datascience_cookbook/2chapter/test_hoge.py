
from unittest import TestCase
from nose.tools import ok_, eq_
from hoge import sum, is_even

class HogeTestCase(TestCase):
    def setup(self):
        print('before test')
    def teardown(self):
        print('after test')
    def test_sum(self):
        eq_(sum(1, 2), 3)
        eq_(sum(5, 11), 16)
        eq_(sum(0, 0), 0)
    def test_is_even(self):
        ok_(is_even(2))
        ok_(not is_even(3))