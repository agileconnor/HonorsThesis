import numpy
import csv

t_file = open('transition_table.csv', 'r')
t_list = list(csv.reader(t_file))

t_list = t_list[1:]
actions = []
for row in t_list:
    state0 = row[1:4]
    state1 = row[4:7]
    actions.append([state0, state1])

print(actions)

transitions = numpy.array(actions)

print(transitions)


