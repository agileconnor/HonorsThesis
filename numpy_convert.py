import numpy
import csv

num_actions = 0

def convertTransitions():
    t_file = open('transition_table.csv', 'r')
    t_list = list(csv.reader(t_file))

    t_list = t_list[1:]
    actions = []
    for row in t_list:
        state0 = row[1:4]
        state1 = row[4:7]
        actions.append([state0, state1])

    print(actions)
    num_actions = len(actions)

    transitions = numpy.array(actions)

    print(transitions)

    return transitions

def convertRewards():
    #Put rewards table stuff here
    r_file = open('rewards_table.csv', 'r')
    r_list = list(csv.reader(r_file))

    r_list = r_list[1:]

def processNetwork(netFile):
    n_file = open(netFile, 'r')

def generateTables(netFile):
    transitions = convertTransitions()
    rewards = convertRewards()


