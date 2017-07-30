"""Test for choose_examine."""
import unittest
from unittest import mock
from borgstractor import borgstractor

LIST_OF_BACKUPS = [
    'test-2017-05-31T23:55:46.769235  Wed, 2017-05-31 23:55:53',
    'test-2017-06-06T06:01:38.286541.checkpoint Tue, 2017-06-06 06:01:46',
    'test-2017-06-07T21:54:51.878745.checkpoint Wed, 2017-06-07 21:54:59',
    'test-2017-06-14T03:48:30.537155.checkpoint Wed, 2017-06-14 03:48:37',
    'test-2017-06-18T23:18:45.527244  Sun, 2017-06-18 23:18:52',
    'test-2017-07-25T17:51:04.315579  Tue, 2017-07-25 17:51:16',
    'test-2017-07-25T23:56:05.218051  Tue, 2017-07-25 23:56:18',
    'test-2017-07-26T15:27:30.978710  Wed, 2017-07-26 15:27:44',
    'test-2017-07-27T03:07:05.311554  Thu, 2017-07-27 03:07:19',
    'test-2017-07-28T20:25:08.672426  Fri, 2017-07-28 20:25:20',
    'test-2017-07-28T22:25:59.117414  Fri, 2017-07-28 22:26:11',
    'test-2017-07-29T00:09:38.157645  Sat, 2017-07-29 00:09:52',
    'test-2017-07-29T02:19:39.006056  Sat, 2017-07-29 02:19:50',
    'test-2017-07-29T04:19:59.024990  Sat, 2017-07-29 04:20:10',
    'test-2017-07-29T16:39:16.110092  Sat, 2017-07-29 16:39:27',
    'test-2017-07-29T18:45:42.862916  Sat, 2017-07-29 18:45:54',
    ]

class TestChoose(unittest.TestCase):
    """test the choose_examine function."""

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_choose_examine(self, mock_input, mock_print):
        mock_input.return_value = '1'
        self.assertEqual(borgstractor.choose_examine(LIST_OF_BACKUPS), 0)
        mock_input.return_value = '4'
        self.assertEqual(borgstractor.choose_examine(LIST_OF_BACKUPS), 3)
        self.assertEqual(borgstractor.choose_examine(LIST_OF_BACKUPS[:1]), 0)
        mock_input.return_value = '200'
        borgstractor.choose_examine(LIST_OF_BACKUPS)
        mock_print.assert_any_call("Out of range.")
        mock_input.return_value = 'garbage'
        

