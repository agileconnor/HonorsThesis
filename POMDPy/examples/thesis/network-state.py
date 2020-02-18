from pomdpy.discrete_pomdp import DiscreteState
from builtins import str

class NetworkState(DiscreteState):
	'''
	NetworkState contains the state of the current node the agent is at in the network.
	'''
	def __init__(self):
		# initialize state
		pass

	def is_adjacent(self, other_state):
		# if another node is adjacent and movable then move to that state
		pass

	def to_string(self):
		print("Implementation Error: implement to_string() in network-state.py")
