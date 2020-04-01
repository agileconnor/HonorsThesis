import mdptoolbox.example
import mdptoolbox

P, R = mdptoolbox.example.rand(12, 4)

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

