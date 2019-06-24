import pytest
from vikingapp.qpf.qpf_manager import QpfManager
from unittest.mock import patch, Mock, MagicMock, mock_open
from pathlib import Path

class TestQpfManager:
    def test_QpfManager_initializes_correctly(self):
        import time
        qpf = QpfManager(testing=True)
        assert qpf.today == time.strftime('%Y%m%d')
        assert len(qpf.qpf_files) == 0

    def test_download_file_locally(self):
        m_filepath = '/tmp/test.grb'
        qpf = QpfManager(testing=True)
        ftp = Mock()
        with patch('vikingapp.qpf.qpf_manager.open', mock_open()) as m_file:
            qpf.download_file_locally(ftp, m_filepath)
            m_file.assert_called_once_with(Path(m_filepath), 'wb')
            ftp.retrbinary.assert_called_once()

    @patch('vikingapp.qpf.qpf_manager.FTP')
    def test_download_2p5km_qpf_grib_files(self, mock_ftp):
        qpf = QpfManager(testing=True)
        hour = '00'
        period = '072'

        mock_files = MagicMock()
        mock_files.return_value = ['p06m_%s%sf%s.grb' % (qpf.today, qpf.hour, period), 'test2.grb']
        mock_ftp.return_value = Mock(
            __enter__=mock_ftp,
            __exit__=Mock(),
            cwd=Mock(),
            login=Mock(),
            nlst=mock_files
        )

        qpf.download_2p5km_data(period, 'test.grb')

        m_ftp = mock_ftp.return_value
        m_ftp.login.assert_called_once()
        m_ftp.cwd.assert_called_once_with('/2p5km_qpf')
        assert len(qpf.qpf_files) == 1

    @patch('vikingapp.qpf.qpf_manager.FTP')
    def test_download_5km_qpf_grib_files(self, mock_ftp):
        qpf = QpfManager(testing=True)
        hour = '00'
        period = '072'

        mock_files = MagicMock()
        mock_files.return_value = ['p06m_%s%sf%s.grb' % (qpf.today, qpf.hour, period), 'test2.grb', 'p06m_%s%sf%s.grb' % (qpf.today, qpf.hour, period)]
        mock_ftp.return_value = Mock(
            __enter__=mock_ftp,
            __exit__=Mock(),
            cwd=Mock(),
            login=Mock(),
            nlst=mock_files
        )
        
        qpf.download_5km_data(period, 'test.grb')
        m_ftp = mock_ftp.return_value
        m_ftp.login.assert_called_once()
        m_ftp.cwd.assert_called_once_with('/5km_qpf')
        assert len(qpf.qpf_files) == 2

    @patch.object(QpfManager, 'download_2p5km_data')
    def test_get_multiple_periods(self, mock_download):
        qpf = QpfManager(testing=True)
        periods = ['06', '12', '18']
        qpf.get_qpf_by_periods(periods)

        assert mock_download.call_count == 3

