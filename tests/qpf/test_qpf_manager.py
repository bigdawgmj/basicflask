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
            qpf._download_file_locally(ftp, m_filepath)
            m_file.assert_called_once_with(Path(m_filepath), 'wb')
            ftp.retrbinary.assert_called_once()

    @patch('vikingapp.qpf.qpf_manager.FTP')
    def test_download_2p5km_qpf_grib_files(self, mock_ftp):
        qpf = QpfManager(testing=True)
        periods = ['006', '012', '018']

        mock_files = MagicMock()
        
        tst_files = ['test2.grb']
        for period in periods:
            tst_files.append('p06m_%s%sf%s.grb' % (qpf.today, qpf.hour, period))
        mock_files.return_value = tst_files

        mock_ftp.return_value = Mock(
            __enter__=mock_ftp,
            __exit__=Mock(),
            cwd=Mock(),
            login=Mock(),
            nlst=mock_files
        )

        qpf._download_qpf_data(periods)

        m_ftp = mock_ftp.return_value
        m_ftp.login.assert_called_once()
        m_ftp.cwd.assert_called_once_with('/2p5km_qpf')
        assert len(qpf.qpf_files) == 3

    @patch('vikingapp.qpf.qpf_manager.FTP')
    def test_download_5km_qpf_grib_files(self, mock_ftp):
        qpf = QpfManager(testing=True)
        qpf.res = '5km_qpf'
        periods = ['012', '018']

        mock_files = MagicMock()
        
        tst_files = ['test1.grb', 'test2.grb']
        for period in periods:
            tst_files.append('p06m_%s%sf%s.grb' % (qpf.today, qpf.hour, period))
        mock_files.return_value = tst_files

        mock_ftp.return_value = Mock(
            __enter__=mock_ftp,
            __exit__=Mock(),
            cwd=Mock(),
            login=Mock(),
            nlst=mock_files
        )

        qpf._download_qpf_data(periods)

        m_ftp = mock_ftp.return_value
        m_ftp.login.assert_called_once()
        m_ftp.cwd.assert_called_once_with('/5km_qpf')
        assert len(qpf.qpf_files) == 2

    # @patch.object(QpfManager, 'download_qpf_data')
    def test_get_by_periods(self):
        qpf = QpfManager(testing=True)
        periods = ['006', '012', '018']
        filenames = qpf._get_qpf_by_periods(periods)
        for i in range(0,3):
            assert periods[i] in filenames[i]

    @patch('vikingapp.qpf.qpf_manager.call')
    def test_prep_grib_to_tiff(self, mock_call):
        qpf = QpfManager(testing=True)
        qpf._prep_grib_to_tiff('test.grb')
        assert mock_call.call_count == 2

    @patch('vikingapp.qpf.qpf_manager.call')
    def test_clip_to_bb(self, mock_call):
        qpf = QpfManager(testing=True)
        bb = {  
                'huc': '001',
                'minx': 0,
                'miny': 0,
                'maxx': 10,
                'maxy': 15
            }
        qpf._clip_to_bb(bb, '0.000833333334000', 'test.tif')
        mock_call.assert_called_once()

    @patch('vikingapp.qpf.qpf_manager.rio')
    def test_convert_in_to_mm(self, mock_rasterio):
        qpf = QpfManager(testing=True)
        qpf._convert_in_to_mm('test.tif')
