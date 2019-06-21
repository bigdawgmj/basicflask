import pytest
from vikingapp.mod.first_ext import FirstExt

class TestFirstExt:
    """ Test class for my first extension """

    def test_some_method(self):
        """ Test for my first extension method """
        assert FirstExt(1, 2).some_method() == 3

    def test_some_other_thing(self):
        assert 5 == 5

