import pytest
from unittest.mock import patch

import vikingapp
from vikingapp import app, init

class TestInit:
    @patch('vikingapp.app.run')
    def test_run_is_called(self, mock_run):
        vikingapp.main()
        assert mock_run.called

    # def test_run_is_called(self):
    #     from vikingapp import __init__
    #     with patch.object(__init__, '__name__', '__main__'):
    #         init()
    # # vikingapp.init()
    #         assert mock_main.called
