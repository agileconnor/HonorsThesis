import sys
import numpy

from network-action import *
from network-observation import *
from network-state import *
from pomdpy.discrete_pomdp import DiscreteActionPool
from pomdpy.discrete_pomdp import DiscreteObservationPool
from pomdpy.pomdp import model


class NetworkModel(model.Model):
	def __init__(self):
		# initial setup of network model variables
		super(NetworkModel, self).__init__()

	def start_scenario(self):
		# begin running test
		pass