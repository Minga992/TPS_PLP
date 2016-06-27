from lexer_rules import tokens

from expressions import *

# diccionario de variables, nombre:tipo
variables = {}

#---------------------------------------------------------#

def p_inicial(expr):
	'start : codigo'
	
	#expr[0] = expr[1]
	#print "inicial\n"

#---------------------------------------------------------#

def p_constante_valor(cte):
	'''constante : STR	
				| BOOL
				| numero
				| LPAREN constante RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if cte[1] == '(':
		cte[0] = cte[2]
	else:	
		if type(cte[1]) == str:
			cte[0] = Constante('str')
		elif type(cte[1]) == bool:
			cte[0] = Constante('bool')
		else: # es un numero
			cte[0] = Constante(cte[1].tipo)

#---------------------------------------------------------#
	
def p_constante_funcion(f):
	'constante : funcion'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	f[0] = Funcion(f[1].tipo)

#---------------------------------------------------------#

def p_variable(expr):
	'''variable : VAR
				| VAR LCORCH NUM RCORCH
				| LPAREN variable RPAREN'''
	#'			| VAR PUNTO VAR'
	
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	#print "variable\n"
	global variables

	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 2:
		expr[0] = Variable(expr[1]) #nombre
	elif len(expr) == 5: # vector
		expr[0] = Variable(expr[1])
		if not(expr[1] in variables):	# si es la primera vez que trato con este vector, aviso
			variables[expr[0].nombre] = 'vector'
		
		
	#elif len(expr) == 4:
		#variables[expr[1]] = 'registro'	# ver que pasa con el campo
	#else:
		#if expr[1] in variables:
			#if variables[expr[1]] != 'vector'+expr[0].tipo:
				#raise SyntaxError
		#else:
			#variables[expr[1]] = 'vector'+expr[0].tipo
	
#---------------------------------------------------------#
	
def p_numero(num):
	'''numero : NUM
			| NUM PUNTO NUM
			| MAS NUM
			| MENOS NUM
			| MAS NUM PUNTO NUM
			| MENOS NUM PUNTO NUM'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(num) <= 2 :
		num[0] = Numero('int')
	else:
		num[0] = Numero('float')
	
	#if num[1] == '+':
		#if len(num) == 3:
			#num[0] = Numero(+num[2],int)
		#else:
			#num[0] = Numero(float('+'+str(num[2])+'.'+str(num[4])),float)
	#elif num[1] == '-':
		#if len(num) == 3:
			#num[0] = Numero(-num[2],int)
		#else:
			#num[0] = Numero(float('-'+str(num[2])+'.'+str(num[4])),float)
	#else:
		#if len(num) == 2:
			#num[0] = Numero('int')
		#else:
			#num[0] = Numero(float(str(num[2])+'.'+str(num[4])),float)
	
#---------------------------------------------------------#
	
def p_zeta(expr):
	'''z : variable
		| constante
		| operacion
		| vector'''
	#'  | registro
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#print "zeta"
	
	expr[0] = expr[1]
	
#---------------------------------------------------------#
	
def p_ge(expr):
	'''g : variable
		| constante 
		| relacion
		| logico'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	expr[0] = expr[1]

#---------------------------------------------------------#

def p_vector(expr):
	'''vector : LCORCH constante separavec RCORCH
			| LCORCH vector separavec RCORCH
			| LPAREN vector RPAREN'''
			
			#| LCORCH registro separavec RCORCH
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif (expr[2].tipo != expr[3].tipo) & (expr[3].tipo != 'vacio'):
		raise SyntaxError
	else:
		expr[0] = Vector('vector'+expr[2].tipo)

#---------------------------------------------------------#

def p_separavector(expr):
	'''separavec : empty
				| COMA constante separavec
				| COMA vector separavec'''
				#| registro separavec'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2:
		expr[0] = Vector('vacio')
	elif (expr[2].tipo != expr[3].tipo) & (expr[3].tipo != 'vacio') :
		raise SyntaxError
	else:
		expr[0] = Vector(expr[2].tipo)

#---------------------------------------------------------#
#
#def p_registro(expr):
	#'registro : LLLAVE RLLAVE'
	#'		  | LLLAVE VAR DOSPTOS constante separareg RLLAVE'
	#'		  | LLLAVE VAR DOSPTOS vector separareg RLLAVE'
	#'		  | LLLAVE VAR DOSPTOS registro separareg RLLAVE'
	#'		  | LPAREN registro RPAREN'
	#
	#if expr[1] == '(':
		#expr[0] = expr[2]
	#elif len(expr) == 3 : 
		#expr[0] = Registro([],[])
	#else:
		#expr[0] = Registro([expr[2].nombre]+expr[5].campos,[expr[2].tipo]+expr[5].tipos)
		#
#---------------------------------------------------------#
#
#def p_separaregistro(expr):
	#'separaReg : empty'
	#'		   | COMA VAR DOSPTOS constante separareg'
	#'		   | COMA VAR DOSPTOS vector separareg'
	#'		   | COMA VAR DOSPTOS registro separareg'
	#
	#if len(expr) == 2 :
		#expr[0] = Registro([],[])
	#else:
		#expr[0] = Registro([expr[4].nombre]+expr[5].campos,[expr[4].tipo]+expr[5].tipos)
	#
#---------------------------------------------------------#

def p_asignacion(expr):
	'''asignacion : variable operasig z
				| variable operasig ternario'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#if type(expr[3]) == Variable:
		#tipoZ = variables[expr[3].nombre]
	#else:
		#tipoZ = expr[3].tipo
	#print expr[0]
	#print expr[1]
	#print expr[2]
	#print expr[3]
	#print len(expr)
	
	global variables
	tipoZ =	tipo_segun(expr[3])
	#print "tengotipo"
	if expr[2] == '=':	# asigno una variable -> inicializo o piso su tipo
		#print "voyaasignartipo"
		if (expr[1].nombre in variables):
			#print "deberia estar aca"
			if variables[expr[1].nombre] == 'vector': # si estoy haciendo var[numero] = bla por primera vez, pongo el tipo vectorbla
				#print variables[expr[1].nombre]
				variables[expr[1].nombre] += tipoZ
			elif variables[expr[1].nombre][:6] == 'vector': # si ya habia hecho var[numero] = bla o var = [bla], veo que matchee el tipo de ahora
				#print variables[expr[1].nombre][6:]
				#print tipoZ
				#print variables[expr[1].nombre][6:] != tipoZ
				if variables[expr[1].nombre][6:] != tipoZ:
					#print "holaaaa"
					raise SyntaxError
				#print variables[expr[1].nombre]
			else:	# es una variable cualquiera, no vector
				variables[expr[1].nombre] = tipoZ
		else:
			variables[expr[1].nombre] = tipoZ
		
		#print variables[expr[1].nombre]
	
	else:	# aca la variable ya deberia estar inicializada
		if not(expr[1].nombre in variables):
			raise SyntaxError
		else:
			tipoV = variables[expr[1].nombre]
			#print tipoV
			if expr[2] == '+=': # es numerico o cadena
				if not((numericos(tipoV,tipoZ)) | ((tipoV == tipoZ) & (tipoZ == 'str'))):
					raise SyntaxError
			else: # es numerico
				if not(numericos(tipoV,tipoZ)):
					raise SyntaxError

#---------------------------------------------------------#	

def p_operasig(op):
	'''operasig : IGUAL
				| MAS IGUAL
				| MENOS IGUAL
				| POR IGUAL
				| DIV IGUAL'''
	
	#print "operasig"
	
	op[0] = op[1]
	if len(op) == 3:
		op[0] += op[2]
	
#---------------------------------------------------------#

def p_matematico(expr):
	'''matematico : z operMatBinario z
				| operMatUnario variable
				| variable operMatUnario
				| LPAREN matematico RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	global variables

	if len(expr) == 4: 
		
		if expr[1] == '(':
			expr[0] = expr[2]
		
		else: 
			tipoZ1 = tipo_segun(expr[1])
			tipoZ2 = tipo_segun(expr[3])
				
			if expr[2] == '+': # es numerico o cadena
				if not((numericos(tipoZ1,tipoZ2)) | ((tipoZ1 == tipoZ2) & (tipoZ2 == 'str'))):
					raise SyntaxError
			elif expr[2] == '%':
				if not((tipoZ1 == 'int') & (tipoZ1 == tipoZ2)):
					raise SyntaxError
			else: # es numerico
				if not(numericos(tipoZ1,tipoZ2)):
					raise SyntaxError
			
			if (tipoZ1 == 'float') | (tipoZ2 == 'float'):
				expr[0] = Operacion('float')
			else:
				expr[0] = Operacion(tipoZ1)
		
	else: # es entero
		if (expr[1] == '++') | (expr[1] == '--') :
			if variables[expr[2]] != 'int':
				raise SyntaxError
		elif variables[expr[1]] != 'int':
			raise SyntaxError
		
		expr[0] = Operacion['int']
		
#---------------------------------------------------------#

def p_operMatBinario(op):
	'''operMatBinario : MAS
					| MENOS
					| POR
					| POT
					| MOD
					| DIV'''
					
	op[0] = op[1]

#---------------------------------------------------------#

def p_operMatUnario(op):
	'''operMatUnario : MAS MAS
					| MENOS MENOS'''
					
	op[0] = op[1]
	op[0] += op[2]

#---------------------------------------------------------#

def p_relacion(expr):
	'''relacion : z operRelacion z
				| LPAREN relacion RPAREN'''
			  
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':
		expr[0] = expr[2]
		
	else:
		tipoZ1 = tipo_segun(expr[1])
		tipoZ2 = tipo_segun(expr[3])
		
		if len(expr[2]) == 1: # para < y > solo numericos
			if not(numericos(tipoZ1,tipoZ2)):
				raise SyntaxError
		else:
			if (tipoZ1 != tipoZ2): # para == y != vale cualquier tipo siempre y cuando sean los dos el mismo
				raise SyntaxError
		
		expr[0] = Operacion('bool')	
		
#---------------------------------------------------------#

def p_operRelacion(op):
	'''operRelacion : IGUAL IGUAL
					| ADM IGUAL
					| MAYOR
					| MENOR'''
					
	op[0] = op[1]
	if len(op) == 3:
		op[0] += op[2]
	
#---------------------------------------------------------#

def p_logico(expr):
	'''logico : z operLogicoBinario z
			| NOT z
			| LPAREN logico RPAREN'''
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3:	# not
		if tipo_segun(expr[2]) != 'bool':
			raise SyntaxError
	elif (tipo_segun(expr[1]) != 'bool') & (tipo_segun(expr[3].tipo) != 'bool'):
		raise SyntaxError
	else:
		expr[0] = Operacion('bool')
	
#---------------------------------------------------------#

def p_operLogBinario(op):
	'''operLogicoBinario : AND
						| OR'''
						
	op[0] = op[1]

#---------------------------------------------------------#

def p_ternario(expr):
	'''ternario : LPAREN constante RPAREN PREG z DOSPTOS z
				| LPAREN constante RPAREN PREG ternario DOSPTOS ternario
				| LPAREN relacion RPAREN PREG z DOSPTOS z
				| LPAREN relacion RPAREN PREG ternario DOSPTOS ternario
				| LPAREN logico RPAREN PREG z DOSPTOS z
				| LPAREN logico RPAREN PREG ternario DOSPTOS ternario
				| LPAREN variable RPAREN PREG z DOSPTOS z
				| LPAREN variable RPAREN PREG ternario DOSPTOS ternario'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoG = tipo_segun(expr[2])
	tipoZ1 = tipo_segun(expr[5])
	tipoZ2 = tipo_segun(expr[7])
	
	if (tipoG != 'bool') | (tipoZ1 != tipoZ2):
		raise SyntaxError
	else:
		expr[0] = Operacion(tipoZ1)

#---------------------------------------------------------#

def p_operacion(expr):
	'''operacion : matematico
				| relacion
				| logico'''
	
	expr[0] = expr[1]

#---------------------------------------------------------#	

def p_sentencia_stipo(expr):
	'''sentencia : asignacion PTOCOMA
				| PRINT z PTOCOMA'''
				
	#print "sentencia\n"
	
#---------------------------------------------------------#

def p_sentencia_ctipo(expr):
	'''sentencia : operMatUnario variable PTOCOMA
				| variable operMatUnario PTOCOMA'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	global variables
	
	if (expr[1] == '++') | (expr[1] == '--') :
		if variables[expr[2]] != 'int':
			raise SyntaxError
		elif variables[expr[1]] != 'int':
			raise SyntaxError
	
	expr[0] = Operacion('int')
	
#---------------------------------------------------------#

def p_bloque(expr):
	'''bloque : LLLAVE codigo RLLAVE
			| sentencia 
			| condicional
			| bucle'''
	
#---------------------------------------------------------#

def p_funcion_multesc(expr):
	'''funcion : MULTESC LPAREN z COMA z RPAREN
				| MULTESC LPAREN z COMA z COMA z RPAREN'''
	
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	tipoZ3 = tipo_segun(expr[7])
	
	if (tipoZ1[:6] != 'vector') | (not(numericos(tipoZ1[6:],tipoZ2))):
		raise SyntaxError
	
	if len(expr) == 9:
		if tipoZ3 != 'bool':
			raise SyntaxError
			
	if (tipoZ1[6:] == 'float') | (tipoZ2 == 'float'):
		expr[0] = Funcion('vectorfloat')
	else:
		expr[0] = Funcion('vectorint')
	
#---------------------------------------------------------#
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#print expr[3]
	
	if tipo_segun(expr[3]) != 'str':
		raise SyntaxError
		
	expr[0] = Funcion('str')
	
#---------------------------------------------------------#

def p_funcion_colin(expr):
	'funcion : COLIN LPAREN z COMA z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	
	if (tipoZ1[:6] != 'vector') | (tipoZ2[:6] != 'vector'): # vectores
		raise SyntaxError
	elif (tipoZ1[-3:] != 'int') & (tipoZ1[-5:] != 'float') & (tipoZ2[-3:] != 'int') & (tipoZ2[-5:] != 'float'): # numericos
		raise SyntaxError
	
	expr[0] = Funcion('bool')

#---------------------------------------------------------#

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#if (expr[3].tipo != 'vector') | (expr[3].tipo != 'str'):  # ojo q vale vector de lo q sea
	if (tipo_segun(expr[3]) != 'str') | (tipo_segun(expr[3])[:6] != 'vector'): 
		raise SyntaxError
	
	expr[0] = Funcion('int')

#---------------------------------------------------------#

def p_condicional(expr):
	'''condicional : IF LPAREN g RPAREN bloque
				| IF LPAREN g RPAREN bloque ELSE bloque'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'bool':
		raise SyntaxError
	
#---------------------------------------------------------#

def p_bucle(expr):
	'''bucle : for
			| while
			| dowhile'''
	
#---------------------------------------------------------#
			
def p_for_sinasig(expr):
	'''for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN bloque
			| FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN bloque
			| FOR LPAREN PTOCOMA g PTOCOMA operMatUnario variable RPAREN bloque
			| FOR LPAREN PTOCOMA g PTOCOMA variable operMatUnario RPAREN bloque'''
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[4]) != 'bool':
		raise SyntaxError
		
	if len(expr) == 10:
		if (expr[6] == '++') | (expr[6] == '--') :
			if variables[expr[7].nombre] != 'int':
				raise SyntaxError
		elif variables[expr[6].nombre] != 'int':
			raise SyntaxError
			
#---------------------------------------------------------#
			
def p_for_conasig(expr):
	'''for : FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN bloque
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN bloque
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA operMatUnario variable RPAREN bloque
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA variable operMatUnario RPAREN bloque'''
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[5]) != 'bool':
		raise SyntaxError
		
	if len(expr) == 11:
		if (expr[7] == '++') | (expr[7] == '--') :
			if variables[expr[8].nombre] != 'int':
				raise SyntaxError
		elif variables[expr[7].nombre] != 'int':
			raise SyntaxError

#---------------------------------------------------------#

def p_while(expr):
	'while : WHILE LPAREN g RPAREN bloque'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'bool':
		raise SyntaxError	

#---------------------------------------------------------#

def p_dowhile(expr):
	'dowhile : DO bloque WHILE LPAREN g RPAREN PTOCOMA'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[5]) != 'bool':
		raise SyntaxError	

#---------------------------------------------------------#

def p_codigo(expr):
	'''codigo : bucle codigo
		    | condicional codigo
	 	    | sentencia codigo
		    | bucle
		    | condicional
		    | sentencia'''

	#print "codigo\n"

#---------------------------------------------------------#

#def p_comentario(expr):
	#'comentario : COMENT'

#---------------------------------------------------------#

def p_empty(p):
	'empty :'
	pass

#---------------------------------------------------------#

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)

#---------------------------------------------------------#

def numericos(tipo1,tipo2):
	#print "numericos"
	return (tipo1 in ['int','float']) & (tipo2 in ['int','float'])


def tipo_segun(objeto):

	global variables
	
	if type(objeto) == Variable:
		variable = variables[objeto.nombre]
	else:
		variable = objeto.tipo
		
	#print "tiposegun"
	return variable
