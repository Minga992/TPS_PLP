class Programa(object):

	def evaluar(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError


class Variable(Programa):
	
	def __init__(self,valor,tipo,nombre):
		#self.valor = valor
		self.tipo = tipo
		#self.nombre = nombre
	

class Constante(Programa):
	
	def __init__(self,valor,tipo):
		self.valor = valor
		self.tipo = tipo
	
	
class Numero(Programa):
	
	def __init__(self,valor,tipo):
		self.valor = valor
		self.tipo = tipo


class Funcion(Programa):
	
	def __init__(self,tipo)
		self.tipo = tipo
	
	
	
class Vector(Programa):
	
	def __init__(self,tipo):
		self.tipo = tipo
		

class SepVec(Vector):
	
	def __init__(self,tipo):
		self.tipo = tipo
		
		
class Registro(Programa):
	
	tipo = 'registro'
	
	def __init__(self,campos,tipos_campos):
		self.campos = campos
		self.tipos_campos = tipos_campos


class SepVec(Registro):
	
class Ternario(Programa):
	
	def __init__(self, tipo):
		self.tipo = tipo
