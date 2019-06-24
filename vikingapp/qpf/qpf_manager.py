import time
from pathlib import Path
from ftplib import FTP
import pdb

class QpfManager:
    DEFAULTS: dict = {'today': None, 'hour': '00', 'output_path': '/tmp/qpf'}
    def __init__(self, qpf_meta=DEFAULTS, testing=False):
        self.today = time.strftime('%Y%m%d') if qpf_meta['today'] is None else qpf_meta['today']
        self.hour = qpf_meta['hour']
        self.qpf_files = []
        self.output_path = Path(qpf_meta['output_path'])
        if not self.output_path.exists() and not testing:
            self.output_path.mkdir()

    def download_file_locally(self, ftp, output_file):
        with open(Path(self.output_path, output_file), 'wb') as grb_file:
            ftp.retrbinary("RETR " + output_file, grb_file.write)

    def download_2p5km_data(self, period, output_file):
        """ Need to get the list of hourly forecasts for the forecast date for the 2.5km """
        with FTP('ftp.wpc.ncep.noaa.gov') as ftp:
            ftp.login()
            ftp.cwd('/2p5km_qpf')
            self.qpf_files = [x for x in ftp.nlst() if 'p06m_%s%sf%s' % (self.today, self.hour, period) in x]
            for q_file in self.qpf_files:
                self.download_file_locally(ftp, q_file)

    def download_5km_data(self, period, output_file):
        """ Need to get the list of hourly forecasts for the forecast date for the 5km """
        with FTP('ftp.wpc.ncep.noaa.gov') as ftp:
            ftp.login()
            ftp.cwd('/5km_qpf')
            self.qpf_files = [x for x in ftp.nlst() if 'p06m_%s%sf%s' % (self.today, self.hour, period) in x]
            # with open(output_file, 'wb') as grb_file:
            #     ftp.retbinary("RETR " + grib, grb_file.write)

    def get_qpf_by_periods(self, periods):
        for period in periods:
            self.download_2p5km_data(self.hour, period)

    # def __del__(self):
    #     self.output_path.rmdir()
    #     print('destructor called...')
        

if __name__ == '__main__':
    qpf = QpfManager()
    qpf.download_2p5km_data('072', 'qpf-trial.grb')


