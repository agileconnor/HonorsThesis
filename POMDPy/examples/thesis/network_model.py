import sys
import numpy

from network_action import *
from network_observation import *
from network_state import *
from pomdpy.discrete_pomdp import DiscreteActionPool
from pomdpy.discrete_pomdp import DiscreteObservationPool
from pomdpy.pomdp import model
from pomdpy.util import console, config_parser


class NetNodeType:
	ACCESSIBLE = 0
 	SQL_VULN = 1
	FTP_VULN = 2
	MITM_VULN = 3
	SQL_FTP = 4
	SQL_MITM = 5
	FTP_MITM = 6
	SQL_FTP_MITM = 7
	ROOT = 8
	GOAL = 9

class NetworkModel(model.Model):
	def __init__(self, args):
		# initial setup of network model variables
		super(NetworkModel, self).__init__(args)
		self.network_config = json.load(open(config_parser.network_config, "r"))

		# Collected Data #
		self.unique_nodes_scanned = []
		self.num_scans = 0
		
		# Network Configuration Data #
		self.network_config = json.load(open(config_parser.network_cfg, "r"))
		self.map_text, _ = config_parser.parse_map(self.network_config['layout_file'])
		# read in raw text and build network based on it
		# TBD


	#unfinished
	def start_scenario(self):
		# begin running test
		pass

	# implementation of abstract Model class #
	def create_observation_pool(self, solver):
		return DiscreteObservationPool(solver)

	def is_terminal(self, network_state):
		return self.get_cell_type(network_state) is NetNodeType.GOAL

	#unfinished
	def is_valid(self, state):
		if isinstance(state, NetworkState):
			return self.is_valid_state(state)
		else:
			return False

	#unfinished
	def is_valid_state(self, state):
		pass

	#unfinished
	def get_legal_actions():
		pass

