from builtins import object
from builtins import str
import numpy as np
from pomdpy.pomdp import HistoricalData
from network_action import ActionType
import sys

class NodeData(object):
    def __init__(self, name='', adj_list=[], vuln=0, vuln_list=[]):
        self.name = name
        self.check_count = 0
        self.adj_list = adj_list
        self.vuln = vuln
        self.vuln_list = vuln_list
        self.target_vuln = None
        
    def update_name(self, name):
        self.name = name

    def update_adj_list(self, adj_list):
        self.adj_list = adj_list
    
    def update_vuln(self, vuln):
        self.vuln = vuln

    def update_target_vuln(self, target_vuln):
        self.target_vuln = target_vuln
    
    def to_string(self):
        out = ''
        out += 'Name: '+str(self.name)
        out += '\nCheck count: '+str(self.check_count)
        out += '\nAdjacency:'+str(self.adj_list)
        out += '\nVulnerability: '+str(self.vuln)
        out += '\nVulnerability List:'+str(self.vuln_list)
        out += '\nTarget Vulnerability:'+str(self.target_vuln)
        return out


class HistoricalNetworkData(HistoricalData):
    def __init__(self, model, current_node, all_node_data, solver):
        self.model = model
        self.solver = solver
        self.current_node = current_node
        self.all_node_data = model.node_list.values()
        self.legal_actions = self.generate_legal_actions

    def copy_node_data(self, other_data):
        new_node_data = []
        [new_node_data.append(NodeData()) for _ in other_data]
        for i, j in zip(other_data, new_node_data):
            j.name = i.name
            j.check_count = i.check_count
            j.adj_list = i.adj_list
            j.vuln = i.vuln
            j.vuln_list = i.vuln_list
        return new_node_data

    def copy(self):
        return self.shallow_copy()

    def deep_copy(self):
        return HistoricalNetworkData(self.model, self.current_node, self.all_node_data, self.solver)

    def shallow_copy(self):
        new_node_data = self.copy_node_data(self.all_node_data)
        return HistoricalNetworkData(self.model, self.current_node, new_node_data, self.solver)

    def update(self, other_belief):
        self.all_node_data = other_belief.data.all_node_data

    '''
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
    '''
    def create_child(self, node_action, node_observation):
        next_data = self.deep_copy()
        next_position, is_legal = self.model.make_next_position(self.current_node, node_action.bin_number)
        next_data.current_node = next_position
        node_data = None
        #node_data = next_data.all_node_data[self.current_node]
        for node in next_data.all_node_data:
            print(node.to_string())
            print('')
            if node.name == next_data.current_node:
                node_data = node
                continue

        if node_action.bin_number is ActionType.SCAN:
            if self.model.last_action_scan:
                if node_data.target_vuln == 'sql_vuln':
                    node_action.bin_number = ActionType.SQL_VULN
                elif node_data.target_vuln == 'ftp_vuln':
                    node_action.bin_number = ActionType.FTP_VULN
                elif node_data.target_vuln == 'smtp_vuln':
                    node_action.bin_number = ActionType.SMTP_VULN
                elif node_data.target_vuln == 'vnc_vuln':
                    node_action.bin_number = ActionType.VNC_VULN
                elif int(node_data.vuln) == 16:

                    node_action.bin_number = ActionType.LATERAL_MOVE
            # scan - check observation and make plan accordingly
            #node_type = self.model.get_node_type(self.current_node)
            node_data.check_count += 1
            expected_reward = 0
            target_vuln = None
            if node_observation.sql_vuln:
                expected_reward = self.model.sql_reward
                target_vuln = 'sql_vuln'
            if node_observation.ftp_vuln:
                if self.model.ftp_reward > expected_reward:
                    expected_reward = self.model.ftp_reward
                    target_vuln = 'ftp_vuln'
            if node_observation.smtp_vuln:
                if self.model.smtp_reward > expected_reward:
                    expected_reward = self.model.smtp_reward
                    target_vuln = 'smtp_vuln'
            if node_observation.vnc_vuln:
                if self.model.vnc_reward > expected_reward:
                    expected_reward = self.model.vnc_reward
                    target_vuln = 'vnc_vuln'
            node_data.update_target_vuln(target_vuln)
            self.model.last_action_scan = True
            
            
        if node_action.bin_number is ActionType.LATERAL_MOVE:
            pass
        if (node_action.bin_number is ActionType.SQL_VULN or node_action.bin_number is ActionType.FTP_VULN
            or node_action.bin_number is ActionType.SMTP_VULN or node_action.bin_number is ActionType.VNC_VULN):
            node_data.update_vuln(16)
            if len(self.model.unique_nodes_scanned) == len(self.model.node_list.keys()):
                node_data.update_vuln(17)

        return next_data

    
    def generate_legal_actions(self):
        legal_actions = []
        all_actions = range(0, 7)

        for action in all_actions:
            if action is ActionType.SCAN and self.model.last_action_scan:
                continue
            if action is ActionType.DEPLOY_AGENT:
                continue
            if action is ActionType.LATERAL_MOVE:
                if len(self.model.unique_nodes_scanned) >= len(self.model.node_list):
                    continue
            else:
                legal_actions.append(action)
        return legal_actions
    