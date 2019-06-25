import time
from pathlib import Path
from ftplib import FTP
import pdb
from subprocess import call
import rasterio as rio

class QpfManager:
    DEFAULTS: dict = {
                'today': None,
                'hour': '00',
                'output_path': '/tmp/qpf',
                'res': '2p5km_qpf',
                'periods': ['006', '012', '018', '024', '030', '036', '042', '048', '054', '060', '066', '072']
            }

    def __init__(self, qpf_meta=DEFAULTS, testing=False):
        self.today = time.strftime('%Y%m%d') if qpf_meta['today'] is None else qpf_meta['today']
        self.hour = qpf_meta['hour']
        self.qpf_files = []
        self.output_path = Path(qpf_meta['output_path'])
        self.res = qpf_meta['res']
        if not self.output_path.exists() and not testing:
            self.output_path.mkdir()

    def _download_file_locally(self, ftp, output_file):
        with open(Path(self.output_path, output_file), 'wb') as grb_file:
            ftp.retrbinary("RETR " + output_file, grb_file.write)

    def _download_qpf_data(self, periods=DEFAULTS['periods']):
        """ Need to get the list of hourly forecasts for the forecast date for the 2.5km/5km options """
        with FTP('ftp.wpc.ncep.noaa.gov') as ftp:
            ftp.login()

            if '2p5km_qpf' in self.res:
                ftp.cwd('/2p5km_qpf')
            else:
                ftp.cwd('/5km_qpf')

            ftp_files = ftp.nlst()
            period_files = self._get_qpf_by_periods(periods)
            self.qpf_files = [x for x in ftp_files if x in period_files]

            for q_file in self.qpf_files:
                self._download_file_locally(ftp, q_file)

    def _get_qpf_by_periods(self, periods):
        period_files = []
        for period in periods:
            period_files.append('p06m_%s%sf%s.grb' % (self.today, self.hour, period))
        return period_files

    # TODO: Need to figure file paths for these
    def _prep_grib_to_tiff(self, grib_file):
        tmp_path = Path(self.output_path, 'tmp')
        fin_path = Path(self.output_path, 'final')

        if not tmp_path.exists():
            tmp_path.mkdir()
        if not fin_path.exists():
            fin_path.mkdir()

        tif_name = grib_file.split('.')[0] + '.tif'

        tmp_file = Path(tmp_path, tif_name)
        fin_file = Path(fin_path, tif_name)
        try:
            call(['gdal_translate', '-of','GTiff', Path(self.output_path, grib_file), tmp_file])
        except Exception as e:
            print('GDAL_TRANSLATE (grib_to_tiff): ' + e)

        try:
            call(['gdalwarp', '-t_srs', 'EPSG:4326', '-dstnodata','0', tmp_file, fin_file])
        except Exception as e:
            print('GDALWARP (grib_to_tiff): ' + e)

    def _clip_to_bb(self, bounding_box, res, filename):
        in_file = Path(self.output_path, 'final', filename)
        fin_path = Path(self.output_path, 'output')
        if not fin_path.exists():
            fin_path.mkdir()
        fin_file = Path(fin_path, filename)
        call(['gdalwarp', '-te', str(bounding_box['minx']), str(bounding_box['miny']), str(bounding_box['maxx']), str(bounding_box['maxy']), '-tr', res, res, str(in_file), str(fin_file)])


    # TODO: rasterio convert to mm/hr (this should probably be abstracted because QPE will probably use this as well)
    def _convert_in_to_mm(self, tif_file):
        with rio.open(tif_file) as src:
            data = src.read(1)
            data = data * 25.4

    # def __del__(self):
    #     self.output_path.rmdir()
    #     print('destructor called...')

if __name__ == '__main__':
    qpf = QpfManager()
    qpf.output_path = Path('/Users/jens402/qfiles')

    if not qpf.output_path.exists():
        qpf.output_path.mkdir()

    qpf._download_qpf_data()
    grib_file = 'p06m_2019062500f012.grb'
    tif_file = 'p06m_2019062500f012.tif'

    qpf._prep_grib_to_tiff(grib_file)
    bb = {
            'minx': -90.047,
            'miny': 28.972,
            'maxx': -82.635,
            'maxy': 32.922
        }
    qpf._clip_to_bb(bb, '0.000833333334000', tif_file)
