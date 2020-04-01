### MDP Code

This is a folder for the older MDP program which does not provide the desired
functionality for this project.

As configured the MDP system using *pymdptoolbox* relies on the series of .csv
files around this directory for running the algorithm. These translate directly
into NumPy arrays.

- network.csv: Contains the description on the network and associated vulnerabilities
- rewards\_table.csv: Contains the awards for each action's success
- transition\_table.csv: Contains the transition table for the MDP. A matrix of probabilities
