import sys
import numpy as np
import json

from network_action import *
from network_observation import NetworkObservation
from network_state import *
from network_position_history import NodeData, HistoricalNetworkData
from pomdpy.discrete_pomdp import DiscreteActionPool
from pomdpy.discrete_pomdp import DiscreteObservationPool
from pomdpy.pomdp import Model
from pomdpy.util import console, config_parser


class NetNodeType:
    ACCESSIBLE = 0
    SQL_VULN = 1
    FTP_VULN = 2
    SMTP_VULN = 3
    VNC_VULN = 4
    SQL_FTP = 5
    SQL_SMTP = 6
    SQL_VNC = 7
    FTP_SMTP = 8
    FTP_VNC = 9
    SMTP_VNC = 10
    SQL_FTP_SMTP = 11
    SQL_FTP_VNC = 12
    SQL_SMTP_VNC = 13
    FTP_SMTP_VNC = 14
    SQL_FTP_SMTP_VNC = 15
    ROOT = 16
    GOAL = 17

class NetworkModel(Model):
    def __init__(self, args):
        # initial setup of network model variables
        super(NetworkModel, self).__init__(args)
        
        # Collected Data #
        self.unique_nodes_scanned = []
        self.num_scans = 0
        
        # Network Configuration Data #
        self.network_config = json.load(open(config_parser.network_cfg, "r"))
        # read in reward values for 4 vulns
        self.sql_reward = 10
        self.ftp_reward = 10
        self.smtp_reward = 10
        self.vnc_reward = 10
        self.map_text, _ = config_parser.parse_map(self.network_config['layout_file'])
        self.node_list = {}
        # read in raw text and build network based on it
        state = 0
        for item in self.map_text:
            if state == 0:
                if item == 'Node Type':
                    state = 1
                    continue
            if state == 1:
                if item == 'Adjacency':
                    state = 2
                    continue
                else:
                    stuff = item.split(':')
                    if stuff[0] not in self.node_list.keys():
                        self.node_list[stuff[0]] = NodeData(stuff[0], [], stuff[1], [])
            if state == 2:
                if item == 'end':
                    break
                else:
                    adj = item.split(' ')
                    for node in self.node_list.values():
                        if node.name == adj[0]:
                            node.update_adj_list(adj[1:])
        
        for node in self.node_list.values():
            print(node.to_string())
            print(' ')


    def get_node_type(self, node_name):
        for node in self.node_list:
            if node.name == node_name:
                return node.vuln
        return -1

    def start_scenario(self):
        # begin running test
        pass

    # implementation of abstract Model class #
    def create_observation_pool(self, solver):
        return DiscreteObservationPool(solver)

    # come back to this one
    def is_terminal(self, node_name):
        return self.get_node_type(node_name) is NetNodeType.GOAL

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
    def get_legal_actions(self):
        pass

    def reset_for_simulation(self):
        """
        The Simulator (Model) should be reset before each simulation
        :return:
        """
        pass

    def reset_for_epoch(self):
        """
        Defines behavior for resetting the simulator before each epoch
        :return:
        """
        pass

    def update(self, sim_data):
        """
        Update the state of the simulator with sim_data
        :param sim_data:
        :return:
        """
        pass

    def generate_step(self, state, action):
        """
        Generates a full StepResult, including the next state, an observation, and the reward
        *
        * For convenience, the action taken is also included in the result, as well as a flag for
        * whether or not the resulting next state is terminal.
        :param state:
        :param action:
        :return: StepResult
        """
        pass

    def sample_an_init_state(self):
        """
        Samples an initial state from the initial belief.
        :return: State
        """
        pass

    def sample_state_uninformed(self):
        """
        Samples a state from a poorly-informed prior. This is used by the provided default
        implementation of the second generateParticles() method.
        :return:
        """
        pass

    def sample_state_informed(self, belief):
        """
        :param belief:
        :return:
        """
        pass

    def belief_update(self, old_belief, action, observation):
        """
        Use bayes filter to update belief distribution
        :param old_belief:
        :param action
        :param observation
        :return:
        """
        pass

    def get_all_states(self):
        """
        :return: list of enumerated states (discrete) or range of states (continuous)
        """
        pass
     
    def get_all_actions(self):
        """
        :return: list of enumerated actions (discrete) or range of actions (continuous)
        """
        pass

    def get_all_observations(self):
        """
        :return: list of enumerated observations (discrete) or range of observations (continuous)
        """
        pass

    def create_action_pool(self):
        """
        :param solver:
        :return:
        """
        pass

    def create_root_historical_data(self, solver):
        """
        reset smart data for the root of the belief tree, if smart data is being used
        :return:
        """
        pass

    def get_max_undiscounted_return(self):
        """
        Calculate and return the highest possible undiscounted return
        :return:
        """
        pass

    def make_next_position(self, current_node, action_type):
        is_legal = True
        next_node = current_node
        if action_type is ActionType.SCAN:
            pass
        elif action_type is ActionType.LATERAL_MOVE:
            if current_node not in self.unique_nodes_scanned:
                self.unique_nodes_scanned.append(current_node)
            for node in self.node_list.keys():
                if node not in self.unique_nodes_scanned:
                    next_node = node 

        return next_node, is_legal
    