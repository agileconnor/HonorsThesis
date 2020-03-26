from pomdpy.discrete_pomdp import DiscreteState
from builtins import str

class NetworkState(DiscreteState):
    def __init__(self, current_node, node_states):
        # initialize state
        if node_states is not None:
            assert node_states.__len__() is not 0
        self.current_node = current_node
        self.node_states = node_states

    def __eq__(self, other_network_state):
        return self.current_node == other_network_state.current_node and self.node_states is other_network_state.node_states

    def copy(self):
        return NetworkState(self.current_node, self.node_states)

    def to_string(self):
        return str(self.current_node)+'\n'+str(self.node_states)

    def as_list(self):
        pass

    def print_state(self):
        pass
