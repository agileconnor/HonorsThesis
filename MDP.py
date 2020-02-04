import mdptoolbox.example
import mdptoolbox
import numpy_convert

P = numpy_convert.convert()

print("Transition Array")
print(P)
print("Reward Array")
print(R)

print("Running MDP Policy Iteration")

pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.9)
pi.setVerbose()
pi.run()

print("Final Policy")
print(pi.policy)
