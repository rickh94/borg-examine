"""Tests for get_backups."""
import unittest
from unittest import mock
import datetime
from borgstractor import get_backups

class DatedInfoTest(unittest.TestCase):

    def setUp(self):
        self.today = datetime.datetime.today()
        self.yesterday = (datetime.datetime.today()
            - datetime.timedelta(days=1))
        self.y2k = datetime.datetime(
            1999, 12, 31, 23, 59, 59)

        self.todaystring = self.today.strftime("Today at %I:%M %p")
        self.yesterdaystring = self.yesterday.strftime("Yesterday at %I:%M %p")
        self.y2kstring = self.y2k.strftime("%a, %b %d, %Y at %I:%M %p")

    def test_pretty_date(self):
        """Tests pretty date."""
        # test today
        todaytest = get_backups.DatedInfo('test_today', self.today)
        self.assertEqual(todaytest.pretty_date(), self.todaystring)
        # test yesterday
        yesterdaytest = get_backups.DatedInfo('test_yesterday', self.yesterday)
        self.assertEqual(yesterdaytest.pretty_date(), self.yesterdaystring)
        # test y2k
        y2ktest = get_backups.DatedInfo('test_y2k', self.y2k)
        self.assertEqual(y2ktest.pretty_date(), self.y2kstring)

class BackupTest(self):

    def setUp(self):
        self.today = datetime.datetime.today()
        self.yesterday = (datetime.datetime.today()
            - datetime.timedelta(days=1))
        self.y2k = datetime.datetime(
            1999, 12, 31, 23, 59, 59)

        self.todaystring = self.today.strftime("Today at %I:%M %p")
        self.yesterdaystring = self.yesterday.strftime("Yesterday at %I:%M %p")
        self.y2kstring = self.y2k.strftime("%a, %b %d, %Y at %I:%M %p")


    @mock.patch('builtins.print')
    def mount(self, mock_print):
        test1 = get_backups.Backup('test1', self.today)


