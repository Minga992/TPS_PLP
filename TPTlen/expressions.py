#'STR'

class NUM(Expr):
	def __init__(self, value):
		self.value = value
		
	def evaluate(self):
		return self.value
