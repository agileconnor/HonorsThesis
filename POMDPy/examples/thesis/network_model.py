import sys
import numpy as np
import json

from network_action import *
from network_observation import NetworkObservation
from network_state import *
from network_position_history import NodeData, HistoricalNetworkData
from pomdpy.discrete_pomdp import DiscreteActionPool
from pomdpy.discrete_pomdp import DiscreteObservationPool
from pomdpy.pomdp import Model, StepResult
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
        self.last_action_scan = False
        self.fresh = True
        
        # Collected Data #
        self.unique_nodes_scanned = []
        self.num_scans = 0
        
        # Network Configuration Data #
        self.network_config = json.load(open(config_parser.network_cfg, "r"))
        # read in reward values for 4 vulns
        self.sql_reward = int(self.network_config['sql_reward'])
        self.ftp_reward = int(self.network_config['ftp_reward'])
        self.smtp_reward = int(self.network_config['smtp_reward'])
        self.vnc_reward = int(self.network_config['vnc_reward'])
        self.scan_reward = int(self.network_config['scan_reward'])
        self.move_reward = int(self.network_config['move_reward'])
        self.exit_reward = int(self.network_config['exit_reward'])
        self.illegal_move_penalty = int(self.network_config['illegal_move_penalty'])
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


    def get_node_type(self, node_in):
        for node in self.node_list.values():
            if node == node_in:
                return node.vuln
        return -1

    # implementation of abstract Model class #
    def create_observation_pool(self, solver):
        return DiscreteObservationPool(solver)

    def is_terminal(self, node_name):
        if self.get_node_type(node_name.current_node) is NetNodeType.GOAL:
            return True
        elif (len(self.unique_nodes_scanned) == len(self.node_list.keys())
            and self.get_node_type(node_name.current_node) is NetNodeType.ROOT):
            return True
        return False

    def is_valid(self, state):
        if isinstance(state, NetworkState):
            return self.is_valid_state(state)
        else:
            return False

    def is_valid_state(self, state):
        return (state.current_node in self.node_list.keys())

    def get_legal_actions(self, state):
        legal_actions = []
        all_actions = range(0, 7)

        for action in all_actions:
            if action is ActionType.DEPLOY_AGENT:
                continue
            if action is ActionType.LATERAL_MOVE:
                if len(self.unique_nodes_scanned) >= len(self.node_list):
                    continue
            else:
                legal_actions.append(action)
        return legal_actions

    def reset_for_simulation(self):
        self.reset_for_epoch()

    def reset_for_epoch(self):
        self.fresh = True
        self.last_action_scan = False

    def update(self, step_result):
        """
        Update the state of the simulator with sim_data
        :param sim_data:
        :return:
        """
        pass

    def generate_step(self, state, action):
        if action is None:
            print('Tried to generate a step with a null action')
            return None
        elif type(action) is int:
            action = NetworkAction(action)

        result = StepResult()
        result.next_state, is_legal = self.make_next_state(state, action)
        if self.fresh and result.action is not ActionType.SCAN:
            self.fresh = False
            action = NetworkAction(ActionType.SCAN)
        result.action = action.copy()
        if result.action.bin_number is ActionType.SCAN:
            self.last_action_scan = True
        else:
            self.last_action_scan = False
        result.observation = self.make_observation(action, result.next_state)
        result.reward = self.make_reward(state, action, result.next_state, is_legal)
        result.is_terminal = self.is_terminal(result.next_state)
        #print('action')
        #print(result.action.to_string())
        #print('observation')
        #print(result.observation.to_string())
        #print('next state node')
        #print(result.next_state.current_node.to_string())
        #sys.exit(0)
        return result, is_legal

    def sample_an_init_state(self):
        self.unique_nodes_scanned = []
        return NetworkState(self.node_list.values()[0], self.sample_nodes())

    def sample_nodes(self):
        node_states = []
        for i in range(0, len(self.node_list)):
            node_states.append(np.random.random_integers(0, (1 << len(self.node_list)) - 1) & (1 << i))
        return node_states

    def sample_state_uninformed(self):
        """
        Samples a state from a poorly-informed prior. This is used by the provided default
        implementation of the second generateParticles() method.
        :return:
        """
        pass

    def sample_state_informed(self, belief):
        return belief.sample_particle()

    def belief_update(self, old_belief, action, observation):
        pass

    def get_all_states(self):
        return None, 6*len(self.node_list)
     
    def get_all_actions(self):
        all_actions = []
        for code in range(0, 7):
            if self.last_action_scan and code == 0:
                continue
            all_actions.append(NetworkAction(code))
        return all_actions

    def get_all_observations(self):
        return {
            'SQL vulnerability': 0,
            'FTP vulnerability': 1,
            'SMTP vulnerability': 2,
            'VNC vulnerability': 3,
            'No vulnerability': 4
        }, 5

    def create_action_pool(self):
        return DiscreteActionPool(self)

    def create_root_historical_data(self, solver):
        self.create_new_node_data()
        return HistoricalNetworkData(self, self.node_list.keys()[1], self.all_node_data, solver)

    def create_new_node_data(self):
        self.all_node_data = []
        for i in range(0, len(self.node_list.keys())):
            self.all_node_data.append(NodeData())

    def get_max_undiscounted_return(self):
        """
        Calculate and return the highest possible undiscounted return
        :return:
        """
        pass

    def make_next_position(self, current_node, action_type):
        is_legal = True
        next_node = current_node
        if action_type is ActionType.SCAN and not self.last_action_scan:
            pass
        elif action_type is ActionType.LATERAL_MOVE:
            if current_node not in self.unique_nodes_scanned:
                self.unique_nodes_scanned.append(current_node)
            for node in self.node_list.values():
                if node not in self.unique_nodes_scanned:
                    next_node = node 

        return next_node, is_legal

    def make_next_state(self, state, action):
        action_type = action.bin_number
        next_position, is_legal = self.make_next_position(state.current_node, action_type)
        if not is_legal:
            # returns a copy of the current state
            return state.copy(), False

        next_state_node_states = list(state.node_states)

        if action_type is ActionType.SCAN:
            self.num_scans += 1.0

        return NetworkState(next_position, next_state_node_states), True

    def make_observation(self, action, next_state):
        # generate new observation if not scanning a node
        if (action.bin_number is ActionType.SQL_VULN or action.bin_number is ActionType.FTP_VULN
            or action.bin_number is ActionType.SMTP_VULN or action.bin_number is ActionType.VNC_VULN
            or action.bin_number is ActionType.LATERAL_MOVE):
            self.last_action_scan = False
            obs = NetworkObservation()
            return obs
        if next_state.current_node in self.unique_nodes_scanned:
            return NetworkObservation(False, False, False, False)

        # generate observation if scanning a node
        if action.bin_number is ActionType.SCAN:
            self.last_action_scan = True
            if int(next_state.current_node.vuln) == 1:
                return NetworkObservation(True, False, False, False)
            elif int(next_state.current_node.vuln) == 2:
                return NetworkObservation(False, True, False, False)
            elif int(next_state.current_node.vuln) == 3:
                return NetworkObservation(False, False, True, False)
            elif int(next_state.current_node.vuln) == 4:
                return NetworkObservation(False, False, False, True)
            elif int(next_state.current_node.vuln) == 5:
                return NetworkObservation(True, True, False, False)
            elif int(next_state.current_node.vuln) == 6:
                return NetworkObservation(True, False, True, False)
            elif int(next_state.current_node.vuln) == 7:
                return NetworkObservation(True, False, False, True)
            elif int(next_state.current_node.vuln) == 8:
                return NetworkObservation(False, True, True, False)
            elif int(next_state.current_node.vuln) == 9:
                return NetworkObservation(False, True, False, True)
            elif int(next_state.current_node.vuln) == 10:
                return NetworkObservation(False, False, True, True)
            elif int(next_state.current_node.vuln) == 11:
                return NetworkObservation(True, True, True, False)
            elif int(next_state.current_node.vuln) == 12:
                return NetworkObservation(True, True, False, True)
            elif int(next_state.current_node.vuln) == 13:
                return NetworkObservation(True, False, True, True)
            elif int(next_state.current_node.vuln) == 14:
                return NetworkObservation(False, True, True, True)
            elif int(next_state.current_node.vuln) == 15:
                return NetworkObservation(True, True, True, True)
        return NetworkObservation(False, False, False, False)

    def make_reward(self, state, action, next_state, is_legal):
        if not is_legal:
            return -self.illegal_move_penalty

        if self.is_terminal(next_state):
            return self.exit_reward

        if action.bin_number is ActionType.SQL_VULN:
            return self.sql_reward
        elif action.bin_number is ActionType.FTP_VULN:
            return self.ftp_reward
        elif action.bin_number is ActionType.SMTP_VULN:
            return self.smtp_reward
        elif action.bin_number is ActionType.VNC_VULN:
            return self.vnc_reward
        elif action.bin_number is ActionType.SCAN:
            return self.scan_reward
        if action.bin_number is ActionType.LATERAL_MOVE:
            return self.move_reward
        return 0

    def generate_reward(self, state, action):
        next_state, is_legal = self.make_next_state(state, action)
        return self.make_reward(state, action, next_state, is_legal)
    