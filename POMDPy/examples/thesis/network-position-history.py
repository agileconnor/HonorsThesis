from builtins import object
from builtins import str
import numpy as np
from pomdpy.pomdp import HistoricalData
from network_action import ActionType

class NodeData(object):
	def __init__(self, adj_list, vuln=0):
		self.check_count = 0
		self.adj_list = adj_list
		self.vuln = vuln
		
	def to_string(self):
		out = ''
		out += 'Check count: '+str(self.check_count)
		out += '\nAdjacency:'+str(adj_list[1:])
		out += '\nVulnerability: '+str(self.vuln)
		return out


class HistoricalNetworkData(HistoricalData):
	def __init__(self, model, network_position, all_node_data, solver):
		self.model = model
		self.solver = solver
		self.network_position = network_position
		self.all_node_data = all_node_data

	def copy_node_data(other_data):
		new_node_data = []
		[new_node_data.append(NodeData()) for _ in other_data]
		for i, j in zip(other_data, new_node_data):
            j.check_count = i.check_count
            j.vuln = i.vuln
        return new_node_data

	def copy(self):
		return self.shallow_copy()

	def deep_copy(self)
		return HistoricalNetworkData(self.model, self.network_position.copy(), self.all_node_data, self.solver)

	def shallow_copy(self):
		new_node_data = self.copy_node_data(self.all_node_data)
		return HistoricalNetworkData(self.model, self.network_position.copy(), new_node_data, self.solver)

	def update(self, other_belief):
		self.all_rock_data = other_belief.data.all_rock_data

	def create_child(self, node_action, rock_observation):
		next_data = self.deep_copy()
		next_position, is_legal = self.model.make_next_position(self.grid_position.copy(), node_action.bin_number)
		next_data.grid_position = next_position

		if node_action.bin_number is ActionType.SCAN:
			node_no = self.model.get_cell_type(self.network_position)
			# FINISH ME PLEASE #