
from pomdpy.discrete_pomdp import DiscreteObservation

class NetworkObservation(DiscreteObservation):
    def __init__(self, sql_vuln=False, ftp_vuln=False, smtp_vuln=False, vnc_vuln=False):
        super(NetworkObservation, self).__init__(0)
        self.sql_vuln = sql_vuln
        self.ftp_vuln = ftp_vuln
        self.smtp_vuln = smtp_vuln
        self.vnc_vuln = vnc_vuln

    def copy(self):
        return NetworkObservation(self.sql_vuln, self.ftp_vuln, self.smtp_vuln, self.vnc_vuln)

    def __eq__(self, other):
        if self.sql_vuln == other.sql_vuln:
            if self.ftp_vuln == other.ftp_vuln:
                if self.smtp_vuln == other.smtp_vuln:
                    if self.vnc_vuln == other.vnc_vuln:
                        return True
        return False
        
    def to_string(self):
        out = ''
        if self.sql_vuln:
            out += 'SQL vulnerability '
        if self.ftp_vuln:
            out += 'FTP vulnerability '
        if self.smtp_vuln:
            out += 'SMTP vulnerability '
        if self.vnc_vuln:
            out += 'VNC vulnerability '
        if out == '':
            out += 'No vulnerability'
        return out

    def print_observation(self):
        if self.sql_vuln:
            print('SQL vulnerability')
        if self.ftp_vuln:
            print('FTP vulnerability')
        if self.mitm_vuln:
            print('SMTP vulnerability')
        if self.vnc_vuln:
            print('VNC vulnerability')

    def distance_to(self):
        pass
