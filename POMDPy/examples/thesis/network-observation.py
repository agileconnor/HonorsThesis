
from pomdpy.discrete_pomdp import DiscreteObservation

class NetworkObservation(DiscreteObservation):
	def __init__(self, sql_vuln=False, ftp_vuln=False, mitm_vuln=False):
		super(NetworkObservation, self).__init__(0)
		self.sql_vuln = sql_vuln
		self.ftp_vuln = ftp_vuln
		self.mitm_vuln = mitm_vuln

	def copy(self):
		return NetworkObservation(self.sql_vuln, self.ftp_vuln, self.mitm_vuln)

	def __eq__(self, other):
		return (self.sql_vuln == other.sql_vuln and self.ftp_vuln == other.ftp_vuln and self.mitm_vuln == other.mitm_vuln)

	def to_string(self):
		out = ""
		if self.sql_vuln:
			out += "SQL vulnerability"
		if self.ftp_vuln:
			out += "FTP vulnerability"
		if self.mitm_vuln:
			out += "MITM vulnerability"
		if out = "":
			out += "No vulnerability"
		return out

	def print_observation(self):
		if self.sql_vuln:
			print("SQL vulnerability")
		if self.ftp_vuln:
			print("FTP vulnerability")
		if self.mitm_vuln:
			print("MITM vulnerability")


