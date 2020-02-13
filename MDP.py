import mdptoolbox.example
import mdptoolbox
import numpy_convert

P,R = numpy_convert.generateTables('network.csv')

print("Transition Array")
print(P)
print("Reward Array")
print(R)

print(P.shape)
print(R.shape)

print("Running MDP Policy Iteration")

pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.9)
pi.setVerbose()
pi.run()

print("Final Policy")
print(pi.policy)
