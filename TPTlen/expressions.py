class Programa(object):

	def evaluar(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError


class Variable(Programa):
	
	campo = 'None' # si se trata de algo tipo reg.campo
	#def __init__(self,valor,tipo,nombre):
	def __init__(self,nombre):
		#self.valor = valor
		#self.tipo = tipo
		self.nombre = nombre
		
	def nombre_campo(self, nombre):
		self.campo = nombre
	

class Constante(Programa):
	
	#def __init__(self,valor,tipo):
	def __init__(self,tipo):
		#self.valor = valor
		self.tipo = tipo
	
	
class Numero(Constante):
	
	atributo_para_que_compile = 1
	#def __init__(self,tipo):
	#def __init__(self,valor,tipo):
		#self.valor = valor
		#self.tipo = tipo


class Funcion(Constante):
	
	atributo_para_que_compile = 1
	#def __init__(self,tipo):
		#self.tipo = tipo
	

class Operacion(Constante):
	
	atributo_para_que_compile = 1
	
	
class Vector(Constante):
	
	atributo_para_que_compile = 1
	
	#def __init__(self,tipo):
		#self.tipo = tipo
		#


class Registro(Programa):
	
	tipo = 'registro'
	
	def __init__(self,campos,tipos_campos):
		self.campos = campos
		self.tipos_campos = tipos_campos


class Codigo(Programa):
	
	def __init__(self,cant_tabs):
		self.cant_tabs = cant_tabs
