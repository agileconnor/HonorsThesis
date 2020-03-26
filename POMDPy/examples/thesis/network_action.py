from pomdpy.discrete_pomdp import DiscreteAction
import sys
from builtins import object

class ActionType(object):
    # enumerate actions
    SCAN = 0
    DEPLOY_AGENT = 1
    LATERAL_MOVE = 2
    SQL_VULN = 3
    FTP_VULN = 4
    SMTP_VULN = 5
    VNC_VULN = 6


class NetworkAction(DiscreteAction):
    # child class for network action
    def __init__(self, action_type):
        super(NetworkAction, self).__init__(action_type)
        self.bin_number = action_type

    def copy(self):
        return NetworkAction(self.bin_number)

    def distance_to(self):
        return 0

    def to_string(self):
        out = ''
        if self.bin_number == 0:
            out += 'SCAN'
        elif self.bin_number == 1:
            out += 'DEPLOY AGENT'
        elif self.bin_number == 2:
            out += 'LATERAL MOVE'
        elif self.bin_number == 3:
            out += 'SQL VULNERABILITY'
        elif self.bin_number == 4:
            out += 'FTP VULNERABILITY'
        elif self.bin_number == 5:
            out += 'SMTP VULNERABILITY'
        elif self.bin_number == 6:
            out += 'VNC VULNERABILITY'
        else:
            out += 'UNDEFINED ACTION'
        return out

    def print_action(self):
        if self.bin_number == 0:
            print('SCAN')
        elif self.bin_number == 1:
            print('DEPLOY AGENT')
        elif self.bin_number == 2:
            print('LATERAL MOVE')
        elif self.bin_number == 3:
            print('SQL VULNERABILITY')
        elif self.bin_number == 4:
            print('FTP VULNERABILITY')
        elif self.bin_number == 5:
            print('SMTP VULNERABILITY')
        elif self.bin_number == 6:
            print('VNC VULNERABILITY')
        else:
            print('UNDEFINED ACTION')

