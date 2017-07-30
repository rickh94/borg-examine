import unittest
from unittest import mock
import borgstractor
import borgstractor.settings as settings

@mock.patch('borgstractor.borg_command.os')
@mock.patch('borgstractor.borg_command.subprocess')
class BorgCommandTest(unittest.TestCase):

    def setUp(self):
        setattr(settings, 'repopath', 'test_path')
        setattr(settings, 'mountpoint', 'test_mount')
        setattr(settings, 'passphrase', 'test_pass')

    def test_borg_popen_list(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('Popen', 'list')
        mock_subprocess.Popen.assert_called_once_with(
            ['borg', 'list', 'test_path'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))

    def test_borg_run_list(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('run', 'list')
        mock_subprocess.run.assert_called_once_with(
            ['borg', 'list', 'test_path'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))

    @mock.patch('borgstractor.borg_command.atexit')
    def test_borg_popen_mount(self, mock_atexit, mock_subprocess, mock_os):
        borgstractor.borg_command.create('Popen', 'mount', 'backup_1')
        mock_subprocess.Popen.assert_called_once_with(
            ['borg', 'mount', 'test_path::backup_1', 'test_mount'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))
        mock_atexit.register.assert_called_once_with(
            borgstractor.borg_command.create, 'run', 'umount')

    @mock.patch('borgstractor.borg_command.atexit')
    def test_borg_run_mount(self, mock_atexit, mock_subprocess, mock_os):
        borgstractor.borg_command.create('run', 'mount', 'backup_1')
        mock_subprocess.run.assert_called_once_with(
            ['borg', 'mount', 'test_path::backup_1', 'test_mount'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))
        mock_atexit.register.assert_called_once_with(
            borgstractor.borg_command.create, 'run', 'umount')

    def test_borg_popen_umount(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('Popen', 'umount')
        mock_subprocess.Popen.assert_called_once_with(
            ['borg', 'umount', 'test_mount'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))

    def test_borg_run_umount(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('run', 'umount')
        mock_subprocess.run.assert_called_once_with(
            ['borg', 'umount', 'test_mount'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))

    def test_borg_popen_extract(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('Popen', 'extract', 'backup_1',
            'myfile')
        mock_subprocess.Popen.assert_called_once_with(
            ['borg', 'extract', 'test_path::backup_1', 'myfile'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))

    def test_borg_run_extract(self, mock_subprocess, mock_os):
        borgstractor.borg_command.create('run', 'extract', 'backup_1',
            'myfile')
        mock_subprocess.run.assert_called_once_with(
            ['borg', 'extract', 'test_path::backup_1', 'myfile'],
            stdout=mock_subprocess.PIPE,
            stderr=mock_subprocess.STDOUT,
            env=dict(mock_os.environ, BORG_PASSPHRASE='test_pass'))
