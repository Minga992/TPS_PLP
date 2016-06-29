from lexer_rules import tokens

from expressions import *

# diccionario de variables, nombre:tipo
variables = {}

#---------------------------------------------------------#

def p_inicial(expr):
	'start : codigo'
	
	#expr[0] = expr[1]
	#print "inicial"
	
	#### FORMATO PARA IMPRIMIR ####
	#expr[1] = Codigo(0)
	#expr[0] = expr[1]
	print expr[1].impr

#---------------------------------------------------------#

def p_constante_valor(cte):
	'''constante : STR	
				| BOOL
				| numero
				| LPAREN constante RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "cte"
	if cte[1] == '(':
		cte[0] = Constante(cte[2].tipo)
	else:	
		if type(cte[1]) == str:
			#print 'str'
			cte[0] = Constante('str')
		elif type(cte[1]) == bool:
			#print 'bool'
			cte[0] = Constante('bool')
		else: # es un numero
			#print 'numero'
			cte[0] = Constante(cte[1].tipo)
			
	#### FORMATO PARA IMPRIMIR ####
	
	if cte[1] == '(':
		cte[0].impr = '(' + cte[2].impr + ')'
	else:	
		if type(cte[1]) == str:
			cte[0].impr = cte[1]
		elif type(cte[1]) == bool:
			cte[0].impr = str(cte[1])
		else: # es un numero
			#print cte[1].impr
			cte[0].impr = cte[1].impr

#---------------------------------------------------------#
	
def p_constante_funcion(f):
	'constante : funcion'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	f[0] = Funcion(f[1].tipo)
	
	#### FORMATO PARA IMPRIMIR ####
	
	f[0].impr = f[1].impr

#---------------------------------------------------------#

def p_variable(expr):
	'''variable : VAR
				| RES
				| VAR LCORCH NUM RCORCH
				| LPAREN variable RPAREN
				| VAR PUNTO VAR'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "var"
	global variables

	if expr[1] == '(':	# var -> (var)
		expr[0] = expr[2]
		
	elif len(expr) == 2: # var -> VAR|RES
		if expr[1] in ['res','reS','rEs','rES','Res','ReS','REs','RES']:
			expr[0] = Variable('res')
		else:
			expr[0] = Variable(expr[1]) #nombre
		
	elif len(expr) == 5: # var -> VAR[NUM]
		expr[0] = Variable(expr[1])
		expr[0].array_elem = 1
		if not(expr[1] in variables):	# si es la primera vez que trato con este vector, aviso
			variables[expr[0].nombre] = 'vector'
			
	else: # var -> REGISTRO.CAMPO
		if expr[1] in ['res','reS','rEs','rES','Res','ReS','REs','RES']: # el campo no puede ser res
			p_error(0)
			
		expr[0] = Variable(expr[1])
		#print expr[3]
		expr[0].nombre_campo(expr[3])
		if (expr[1] in variables):
			if type(variables[expr[1]]) != dict: # era otra cosa y ahora es un registro
			#if (variables[expr[1]] != 'registro'):
				#p_error(0)
				variables[expr[1]] = {}
		else:
			variables[expr[1]] = {} # es un registro nuevito
	
	#print expr[1]
	#print variables[expr[1]]
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = expr[0].nombre
		if len(expr) == 4:
			expr[0].impr += '.' + expr[3]
		elif len(expr) == 5: 
			#print expr[3]
			expr[0].impr += '[' + str(expr[3]) + ']'
			
#---------------------------------------------------------#
	
def p_numero(num):
	'''numero : NUM
			| NUM PUNTO NUM
			| MAS NUM
			| MAS NUM PUNTO NUM
			| MENOS NUM
			| MENOS NUM PUNTO NUM'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print num
	if len(num) <= 2 :
		num[0] = Numero('int')
	else:
		num[0] = Numero('float')
		
	#### FORMATO PARA IMPRIMIR ####
	
	if len(num) == 2:
		num[0].impr = str(num[1])
	elif len(num) == 3:
		num[0].impr = num[1] + str(num[2])
	elif len(num) == 4:
		num[0].impr = str(num[1])+'.'+str(num[3])
	else:
		num[0].impr = num[1]+str(num[2])+'.'+str(num[4])
	
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
		| vector
		| registro'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#print "zeta"
	
	expr[0] = expr[1]
	#print expr[0].impr
	#### FORMATO PARA IMPRIMIR ####
	
#---------------------------------------------------------#

def p_zeta_sin_oper(expr):
	'''zso : variable
			| constante
			| vector
			| registro'''
			
	expr[0] = expr[1]

#---------------------------------------------------------#
	
def p_ge(expr):
	'''g : variable
		| constante 
		| relacion
		| logico'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "ge"
	expr[0] = expr[1]

#---------------------------------------------------------#

def p_vector(expr):
	'''vector : LCORCH constante separavec RCORCH
			| LCORCH vector separavec RCORCH
			| LCORCH registro separavec RCORCH
			| LPAREN vector RPAREN'''			
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "vector"
	if expr[1] == '(':
		expr[0] = expr[2]
	elif (expr[2].tipo != expr[3].tipo) & (expr[3].tipo != 'vacio'):
		p_error(0)
	else:
		expr[0] = Vector('vector'+expr[2].tipo)
		
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = '[' + expr[2].impr + expr[3].impr + ']'

#---------------------------------------------------------#

def p_separavector(expr):
	'''separavec : empty
				| COMA constante separavec
				| COMA vector separavec
				| COMA registro separavec'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2:
		expr[0] = Vector('vacio')
	elif (expr[2].tipo != expr[3].tipo) & (expr[3].tipo != 'vacio') :
		p_error(0)
	else:
		expr[0] = Vector(expr[2].tipo)
		
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2:
		expr[0].impr = ', ' + expr[2].impr + expr[3].impr		

#---------------------------------------------------------#

def p_registro(expr):
	'''registro : LLLAVE RLLAVE
				| LLLAVE VAR DOSPTOS constante separareg RLLAVE
				| LLLAVE VAR DOSPTOS vector separareg RLLAVE
				| LLLAVE VAR DOSPTOS registro separareg RLLAVE
				| LPAREN registro RPAREN'''
				
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "registro"
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3 : 
		expr[0] = Registro([],[])
	else:
		expr[0] = Registro([expr[2]]+expr[5].campos,[expr[4].tipo]+expr[5].tipos_campos)
		
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 3 : 
		expr[0].impr = '{}'
	else:
		expr[0].impr = '{' + expr[2] + ': ' + expr[4].impr + expr[5].impr + '}'
		
#---------------------------------------------------------#

def p_separaregistro(expr):
	'''separareg : empty
				| COMA VAR DOSPTOS constante separareg
				| COMA VAR DOSPTOS vector separareg
				| COMA VAR DOSPTOS registro separareg'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) == 2 :
		expr[0] = Registro([],[])
	else:
		#print type(expr[2])
		expr[0] = Registro([expr[2]]+expr[5].campos,[expr[4].tipo]+expr[5].tipos_campos)
		
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2 :
		expr[0].impr = ', ' + expr[2] + ': ' + expr[4].impr + expr[5].impr
	
#---------------------------------------------------------#

def p_asignacion(expr):
	'''asignacion : variable operasig z
				| variable operasig ternario'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "asig"
	global variables
	tipoZ =	tipo_segun(expr[3])
	#print tipoZ
	
	if expr[2] == '=':	# asigno una variable -> inicializo o piso su tipo
		
		if (expr[1].nombre in variables): # si la variable ya se uso antes
			#print expr[1].campo
			if expr[1].campo != 'None': # si es registro.campo = bla
				variables[expr[1].nombre][expr[1].campo] = tipoZ
		
			elif variables[expr[1].nombre] == 'vector': # si estoy haciendo var[numero] = bla por primera vez, pongo el tipo vectorbla
				variables[expr[1].nombre] += tipoZ
				
			elif variables[expr[1].nombre][:6] == 'vector': # si ya habia hecho var[numero] = bla o var = [bla], veo que matchee el tipo de ahora
				
				if (expr[1].array_elem == 1) & (variables[expr[1].nombre][6:] != tipoZ):
					p_error(0)
				#else:
					
					
			else:	# es una variable cualquiera, no vector
							
				if tipoZ == 'registro':	# reflejo los campos
					variables[expr[1].nombre] = campos_a_dic(expr[3])
					
				else:
					variables[expr[1].nombre] = tipoZ
				
		else:
			
			if tipoZ == 'registro':	# reflejo los campos
				variables[expr[1].nombre] = campos_a_dic(expr[3])
			else:
				variables[expr[1].nombre] = tipoZ
		
	else:	# aca la variable ya deberia estar inicializada
		if not(expr[1].nombre in variables):
			p_error(0)
		else:
			tipoV = variables[expr[1].nombre]

			if expr[2] == '+=': # es numerico o cadena
				if not((numericos(tipoV,tipoZ)) | ((tipoV == tipoZ) & (tipoZ == 'str'))):
					p_error(0)
			else: # es numerico
				if not(numericos(tipoV,tipoZ)):
					p_error(0)
	
	#print expr[1].nombre
	#print variables[expr[1].nombre]
	
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr
	expr[0] = Codigo(0,imprimir)

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
	'''matematico : z operMatBinario zso
				| z operMatBinario LPAREN matematico RPAREN
				| LPAREN matematico RPAREN'''
								#| operMatUnario variable
#| variable operMatUnario
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "mat"
	global variables

	#if len(expr) == 4: 
		
	if expr[1] == '(':
		expr[0] = expr[2]
	
	else: 
		tipoZ1 = tipo_segun(expr[1])
		#print type(expr[1])
		if len(expr)==4:
			tipoZ2 = tipo_segun(expr[3]) # zso
		else: 
			tipoZ2 = tipo_segun(expr[4]) # (mat)
		#print tipoZ1
		#print tipoZ2
			
		if expr[2] == '+': # es numerico o cadena
			if not((numericos(tipoZ1,tipoZ2)) | ((tipoZ1 == tipoZ2) & (tipoZ2 == 'str'))):
				#print tipoZ1
				p_error(0)
		elif expr[2] == '%':
			if not((tipoZ1 == 'int') & (tipoZ1 == tipoZ2)):
				p_error(0)
		else: # es numerico
			if not(numericos(tipoZ1,tipoZ2)):
				p_error(0)
		
		if (tipoZ1 == 'float') | (tipoZ2 == 'float'):
			expr[0] = Operacion('float')
		else:
			expr[0] = Operacion(tipoZ1)
		
	#else: # es entero
		#if (expr[1] == '++') | (expr[1] == '--') :
			#if variables[expr[2]] != 'int':
				#p_error(0)
		#elif variables[expr[1]] != 'int':
			#p_error(0)
		#
		#expr[0] = Operacion['int']
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		imprimir = '(' + expr[2].impr + ')'
	else:
		imprimir = expr[1].impr + ' ' + expr[2] + ' '
		if len(expr) == 4:
			imprimir += expr[3].impr
		else:
			imprimir += '(' + expr[4].impr + ')'
	
	expr[0].impr = imprimir
		
#---------------------------------------------------------#

def p_operMatBinario(op):
	'''operMatBinario : MAS
					| MENOS
					| POR
					| POT
					| MOD
					| DIV'''
	#print "mas"			
	op[0] = op[1]

#---------------------------------------------------------#

def p_operMatUnario(op):
	'''operMatUnario : MAS MAS
					| MENOS MENOS'''
	#print "opmatun"
	op[0] = op[1]
	op[0] += op[2]

#---------------------------------------------------------#

def p_relacion(expr):
	'''relacion : z operRelacion zso
				| z operRelacion LPAREN operacion RPAREN
				| LPAREN relacion RPAREN'''
			  
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':
		expr[0] = expr[2]
		
	else:
		tipoZ1 = tipo_segun(expr[1])
		
		if len(expr) == 4:
			tipoZ2 = tipo_segun(expr[3]) # zso
		else:
			tipoZ2 = tipo_segun(expr[4]) # (oper)
		
		if len(expr[2]) == 1: # para < y > solo numericos
			if not(numericos(tipoZ1,tipoZ2)):
				p_error(0)
		else:
			#print tipoZ1
			#print tipoZ2
			if not(numericos(tipoZ1,tipoZ2) | (tipoZ1 == tipoZ2)) : # para == y != vale cualquier tipo siempre y cuando sean los dos el mismo
				p_error(0)
		
		expr[0] = Operacion('bool')	
		
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		imprimir = '(' + expr[2].impr + ')'
	else:
		imprimir = expr[1].impr + ' ' + expr[2] + ' '
		if len(expr) == 4:
			imprimir += expr[3].impr
		else:
			imprimir += '(' + expr[4].impr + ')'
	
	expr[0].impr = imprimir
		
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
	'''logico : z operLogicoBinario zso
			| z operLogicoBinario LPAREN operacion RPAREN
			| NOT z
			| LPAREN logico RPAREN'''
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3:	# not
		if tipo_segun(expr[2]) != 'bool':
			p_error(0)
	elif (tipo_segun(expr[1]) != 'bool'): #& (tipo_segun(expr[3].tipo) != 'bool'):
		p_error(0)
	elif len(expr) == 4:
		if tipo_segun(expr[3].tipo) != 'bool':	#zso
			p_error(0)
	elif tipo_segun(expr[4].tipo) != 'bool': #  (oper)
		p_error(0)
		
	expr[0] = Operacion('bool')
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 3:	# not
		expr[0].impr = 'NOT ' + expr[2].impr
	elif len(expr) == 4:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr
	else:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + '(' + expr[3].impr + ')'
		
#---------------------------------------------------------#

def p_operLogBinario(op):
	'''operLogicoBinario : AND
						| OR'''
						
	op[0] = op[1]

#---------------------------------------------------------#

def p_ternario(expr):
	'''ternario : g PREG z DOSPTOS z
				| g PREG ternario DOSPTOS ternario'''
				
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoG = tipo_segun(expr[1])
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	
	if (tipoG != 'bool') | (tipoZ1 != tipoZ2):
		p_error(0)
	else:
		expr[0] = Operacion(tipoZ1)
		
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = expr[1].impr + ' ? ' + expr[3].impr + ' : ' + expr[5].impr

#---------------------------------------------------------#

def p_operacion(expr):
	'''operacion : matematico
				| relacion
				| logico'''
	
	#print "oper"
	
	expr[0] = expr[1]

#---------------------------------------------------------#	

def p_autoincdec(expr):
	'''autoincdec : operMatUnario variable
				| variable operMatUnario'''

	if (expr[1] == '++') | (expr[1] == '--') :
		if variables[expr[2].nombre] != 'int':
			p_error(0)
	elif variables[expr[1].nombre] != 'int':
		p_error(0)
		
	#### FORMATO PARA IMPRIMIR ####
	
	if (expr[1] == '++') | (expr[1] == '--') :
		imprimir = expr[1] + expr[2].impr
	else:
		imprimir = expr[1].impr + expr[2]
		
	expr[0] = Codigo(0,imprimir)

#---------------------------------------------------------#	

def p_sentencia_(expr):
	'''sentencia : asignacion PTOCOMA
				| PRINT z PTOCOMA
				| autoincdec PTOCOMA'''
				
	#print "sentencia"
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) == 3:
		imprimir = expr[1].impr + ';\n'
	else:
		imprimir = 'print ' + expr[2].impr + ';\n'
		
	expr[0] = Codigo(0,imprimir)
	
#---------------------------------------------------------#

#def p_sentencia_ctipo(expr):
	#'''sentencia : operMatUnario variable PTOCOMA
				#| variable operMatUnario PTOCOMA'''
	#
	### CHEQUEO Y ASIGNACION DE TIPOS ####
	#print "unario?"
	#global variables
	#
	#if (expr[1] == '++') | (expr[1] == '--') :
		#if variables[expr[2]] != 'int':
			#p_error(0)
		#elif variables[expr[1]] != 'int':
			#p_error(0)
	#
	#expr[0] = Operacion('int')
	#
#---------------------------------------------------------#

def p_bloque(expr):
	'''bloque : LLLAVE codigo RLLAVE
			| sentencia 
			| condicional
			| bucle'''
	
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) == 2:
		imprimir = '\n' + tabular(expr[1].impr)# + '\n'
	else:
		#expr[2].acum_tabs += 1
		#expr[0] = expr[1] + '\n' + expr[2] + '\n' + expr[3]
		imprimir = '{\n' + tabular(expr[2].impr) + '}'
		
	expr[0] = Codigo(0,imprimir)
	
#---------------------------------------------------------#

def p_funcion_multesc(expr):
	'''funcion : MULTESC LPAREN z COMA z RPAREN
				| MULTESC LPAREN z COMA z COMA z RPAREN'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	tipoZ3 = tipo_segun(expr[7])
	
	if (tipoZ1[:6] != 'vector') | (not(numericos(tipoZ1[6:],tipoZ2))):
		p_error(0)
	
	if len(expr) == 9:
		if tipoZ3 != 'bool':
			p_error(0)
			
	if (tipoZ1[6:] == 'float') | (tipoZ2 == 'float'):
		expr[0] = Funcion('vectorfloat')
	else:
		expr[0] = Funcion('vectorint')
		
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'multiplicacionEscalar(' + expr[3].impr + + ', ' + expr[5].impr
	
	if len(expr) == 9:
		expr[0].impr += ', ' + expr[7].impr + ')'
	else:
		expr[0].impr += ')'
	
#---------------------------------------------------------#
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#print expr[3]
	
	if tipo_segun(expr[3]) != 'str':
		p_error(0)
		
	expr[0] = Funcion('str')
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'capitalizar(' + expr[3].impr + ')'
	
#---------------------------------------------------------#

def p_funcion_colin(expr):
	'funcion : COLIN LPAREN z COMA z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	
	if (tipoZ1[:6] != 'vector') | (tipoZ2[:6] != 'vector'): # vectores
		p_error(0)
	elif (tipoZ1[-3:] != 'int') & (tipoZ1[-5:] != 'float') & (tipoZ2[-3:] != 'int') & (tipoZ2[-5:] != 'float'): # numericos
		p_error(0)
	
	expr[0] = Funcion('bool')
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'colineales(' + expr[3].impr + ', ' + expr[5].impr + ')'

#---------------------------------------------------------#

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	#if (expr[3].tipo != 'vector') | (expr[3].tipo != 'str'):  # ojo q vale vector de lo q sea
	if (tipo_segun(expr[3]) != 'str') & (tipo_segun(expr[3])[:6] != 'vector'): 
		p_error(0)
	
	expr[0] = Funcion('int')
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'length(' + expr[3].impr + ')'

#---------------------------------------------------------#

def p_condicional(expr):
	'''condicional : IF LPAREN g RPAREN bloque
				| IF LPAREN g RPAREN bloque ELSE bloque'''
	
	## CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'bool':
		p_error(0)
		
	## FORMATO PARA IMPRIMIR ####
	
	imprimir = 'if(' + expr[3].impr + ')' + expr[5].impr
	
	if len(expr) > 6:
		imprimir += '\nelse' + expr[7].impr
		
	expr[0] = Codigo(0,imprimir)
	
#---------------------------------------------------------#

def p_bucle(expr):
	'''bucle : for
			| while
			| dowhile'''
			
	expr[0] = expr[1]
	
#---------------------------------------------------------#
			
def p_for_sinasig(expr):
	'''for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN bloque
			| FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN bloque
			| FOR LPAREN PTOCOMA g PTOCOMA autoincdec RPAREN bloque'''
			#| FOR LPAREN PTOCOMA g PTOCOMA variable operMatUnario RPAREN bloque'''
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	global variables
	
	if tipo_segun(expr[4]) != 'bool':
		p_error(0)
		
	#if len(expr) == 10:
		#if (expr[6] == '++') | (expr[6] == '--') :
			#if variables[expr[7].nombre] != 'int':
				#p_error(0)
		#elif variables[expr[6].nombre] != 'int':
			#p_error(0)
			
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'for( ; ' + expr[4].impr + '; '
	
	if expr[6] == ')':
		imprimir += ')' + expr[7].impr
	else:
		imprimir += expr[6].impr + ')' + expr[8].impr
		
	expr[0] = Codigo(0,imprimir)
			
#---------------------------------------------------------#
			
def p_for_conasig(expr):
	'''for : FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN bloque
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN bloque
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA autoincdec RPAREN bloque'''
			#| FOR LPAREN asignacion PTOCOMA g PTOCOMA variable operMatUnario RPAREN bloque
			
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	global variables
	
	if tipo_segun(expr[5]) != 'bool':
		p_error(0)
		
	#if len(expr) == 11:
		#if (expr[7] == '++') | (expr[7] == '--') :
			#if variables[expr[8].nombre] != 'int':
				#p_error(0)
		#elif variables[expr[7].nombre] != 'int':
			#p_error(0)
			
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'for(' + expr[3].impr + ' ; ' + expr[5].impr + '; '
	
	if expr[7] == ')':
		imprimir += ')' + expr[7].impr
	else:
		imprimir += expr[7].impr + ')' + expr[9].impr
		
	expr[0] = Codigo(0,imprimir)

#---------------------------------------------------------#

def p_while(expr):
	'while : WHILE LPAREN g RPAREN bloque'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'bool':
		p_error(0)	
		
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'while(' + expr[3].impr + ')' + expr[5].impr
	expr[0] = Codigo(0,imprimir)
	
#---------------------------------------------------------#

def p_dowhile(expr):
	'dowhile : DO bloque WHILE LPAREN g RPAREN PTOCOMA'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[5]) != 'bool':
		p_error(0)	
		
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'do' + expr[2].impr + 'while(' + expr[5].impr + ');\n'
	expr[0] = Codigo(0,imprimir)

#---------------------------------------------------------#

def p_codigo(expr):
	'''codigo : bucle codigo
	 	    | sentencia codigo
	 	    | condicional codigo
	 	    | comentario codigo
		    | bucle
		    | sentencia
		    | condicional
		    | comentario'''

	#print "codigo"
	
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = expr[1].impr
	
	if len(expr) == 3:
		imprimir += expr[2].impr
		
	expr[0] = Codigo(0,imprimir)
	
	#expr[1] = Codigo(expr[0].acum_tabs)
	#
	#expr[0] = imprimir_tabs(expr[0].acum_tabs) + expr[1].impr + '\n'
	#
	#if len(expr) == 3:
		#expr[2] = Codigo(expr[0].acum_tabs)
		#expr[0] += expr[2].impr + '\n'

#---------------------------------------------------------#

def p_comentario(expr):
	'comentario : COMENT'
	
	#### FORMATO PARA IMPRIMIR ####
	
	#expr[0] = Codigo(0,expr[1])

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
    #print "error"
    raise Exception(message)

#---------------------------------------------------------#

def numericos(tipo1,tipo2):
	#print "numericos"
	return (tipo1 in ['int','float']) & (tipo2 in ['int','float'])


def tipo_segun(objeto):

	global variables
	
	if type(objeto) == Variable:
		#print objeto.campo
		if objeto.array_elem == 1:	# es una posicion de un arreglo
			variable = variables[objeto.nombre][6:]
		elif objeto.campo != 'None':	# es algo tipo reg.campo
			print 'alalal'
			variable = variables[objeto.nombre][objeto.campo]
		else:		
			variable = variables[objeto.nombre]
	else:
		variable = objeto.tipo
		
	#print "tiposegun"
	return variable


def campos_a_dic(reg):
	
	dic = {}
	
	for x in range(0,len(reg.campos)):
		dic[reg.campos[x]] =  reg.tipos_campos[x]
		
	return dic

#---------------------------------------------------------#

def imprimir_tabs(cant):
	
	res = ""
	
	for x in range(0,cant):
		res += '\n'

	return res


def tabular(texto):
	
	lineas = texto.splitlines()
	res = ""
	
	for l in lineas:
		res += '\t' + l + '\n'
		
	return res
