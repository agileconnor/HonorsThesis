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
	MITM_VULN = 5


class NetworkAction(DiscreteAction):
	# child class for network action
	def __init__():
		super(NetworkAction, self).__init__(action_type)
		self.bin_number = action_type

	def to_string():
		print("Implementation Error: please implement to_string() in network-action.py")

	def print_action():
		if self.bin_number == 0:
			print("SCAN")
		elif self.bin_number == 1:
			print("DEPLOY AGENT")
		elif self.bin_number == 2:
			print("LATERAL MOVE")
		elif self.bin_number == 3:
			print("SQL VULNERABILITY")
		elif self.bin_number == 4:
			print("FTP VULNERABILITY")
		elif self.bin_number == 5:
			print("MITM VULNERABILITY")
		else:
			print("UNDEFINED ACTION")

