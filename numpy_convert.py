import numpy
import csv

num_actions = 0

def convertTransitions():
    t_file = open('transition_table.csv', 'r')
    t_list = list(csv.reader(t_file))

    t_list = t_list[1:]
    actions = []
    for row in t_list:
        state0 = list(map(float, row[1:4]))
        state1 = list(map(float, row[4:7]))
        state2 = list(map(float, row[7:10]))
        actions.append([state0, state1, state2])

    #print(actions)
    num_actions = len(actions)

    transitions = numpy.array(actions)

    #print(transitions)
    t_file.close()

    return transitions

def convertRewards():
    #Put rewards table stuff here
    r_file = open('rewards_table.csv', 'r')
    r_list = list(csv.reader(r_file))

    r_list = r_list[1:]
    rewards = []
    for row in r_list:
        r1 = list(map(int, row[1:]))
        rewards.append(r1)

    rewards = numpy.array(rewards)
    r_file.close()

    return rewards

def processNetwork(netFile):
    n_file = open(netFile, 'r')
    n_list = list(csv.reader(n_file))

    n_list = n_list[1:]
    computers = []
    for row in n_list:
        computer = list(map(int, row[1:]))
        computers.append(computer)

    n_file.close()
    return computers

def generateTables(netFile):
    transitions = convertTransitions()
    rewards = convertRewards()
    computers = processNetwork(netFile)

    #print(computers)

    arrays = []
    for computer in computers:
        newTran = numpy.copy(transitions)
        for act in range(0, len(computer)):
            #print(act)
            newTran[act] = newTran[act] * computer[act]
        arrays.append(newTran)

    newTransitions = numpy.asarray(arrays)
    #print(newTransitions)
    newTransitions = numpy.mean(newTransitions, axis = 0)

    print("Averaged Transition Table Generated")
    print(newTransitions)

    for action in newTransitions:
        state_num = 0
        for state in action:
            arr_sum = numpy.sum(state)
            if arr_sum == 0.0:
                state[state_num] = 1
            else:
                diff = 1 - arr_sum
                diff = diff / 3
                for substate in range(0, len(state)):
                    state[substate] = state[substate] + diff
            state_num += 1
        

    return [newTransitions, rewards]

