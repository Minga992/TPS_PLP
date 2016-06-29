class Programa(object):

	def evaluar(self):
		# Aca se implementa cada tipo de expresion.
		raise NotImplementedError


class Variable(Programa):
	
	impr = ""
	campo = 'None' # si se trata de algo tipo reg.campo
	array_elem = 0 # si se trata de algo tipo var[num]
	#def __init__(self,valor,tipo,nombre):
	def __init__(self,nombre):
		#self.valor = valor
		#self.tipo = tipo
		self.nombre = nombre
		
	def nombre_campo(self, nombre):
		self.campo = nombre
	

class Constante(Programa):
	
	impr = ""
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
	
	#impr = ""
	#acum_tabs = 0
	def __init__(self,acum_tabs,impr):
		self.acum_tabs = acum_tabs
		self.impr = impr
