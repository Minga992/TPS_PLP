from lexer_rules import tokens

from expressions import *

# diccionario de variables, nombre:tipo
variables = {}

#---------------------------------------------------------#

def p_inicial(expr):
	'start : codigo'

	expr[0] = expr[1]

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_constante_valor(cte):
	'''constante : STR	
				| BOOL
				| numero
				| LPAREN constante RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if cte[1] == '(':
		cte[0] = Constante(cte[2].tipo)
	else:	
		if type(cte[1]) == str:
			cte[0] = Constante('str')
		elif type(cte[1]) == bool:
			cte[0] = Constante('bool')
		else: # es un numero
			cte[0] = Constante(cte[1].tipo)

	#### FORMATO PARA IMPRIMIR ####
	
	if cte[1] == '(':
		cte[0].impr = '(' + cte[2].impr + ')'
	else:	
		if type(cte[1]) == str:
			cte[0].impr = cte[1]
		elif type(cte[1]) == bool:
			cte[0].impr = str(cte[1]).lower()
		else: # es un numero
			cte[0].impr = cte[1].impr

#---------------------------------------------------------#
	
def p_constante_funcion(f):
	'constante : funcion'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	f[0] = Funcion(f[1].tipo)
	
	#### FORMATO PARA IMPRIMIR ####
	
	f[0].impr = f[1].impr

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_variable(expr):
	'''variable : VAR
				| RES
				| variable LCORCH z RCORCH
				| LPAREN variable RPAREN
				| VAR PUNTO VAR'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	global variables

	if expr[1] == '(':	# var -> (var)
		expr[0] = expr[2]
		
	elif len(expr) == 2: # var -> VAR|RES
		if expr[1] in ['res','reS','rEs','rES','Res','ReS','REs','RES']:
			expr[0] = Variable('res')
		else:
			expr[0] = Variable(expr[1]) #nombre

	elif len(expr) == 5: # var -> var[NUM]
		if tipo_segun(expr[3]) != 'int':
			error_semantico(expr,3,"El indice del vector debe ser entero")
			
		expr[0] = expr[1]
		expr[0].array_elem += 1

	else: # var -> REGISTRO.CAMPO
		if expr[1] in ['res','reS','rEs','rES','Res','ReS','REs','RES']: # el campo no puede ser res
			error_semantico(expr,1,"El campo no puede ser una palabra reservada")

		expr[0] = Variable(expr[1])
		expr[0].nombre_campo(expr[3])
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 5: 
		expr[0].impr = expr[1].impr + '[' + expr[3].impr + ']'
	else:
		expr[0].impr = expr[0].nombre
		if len(expr) == 4:
			expr[0].impr += '.' + expr[3]

#---------------------------------------------------------#
#---------------------------------------------------------#
	
def p_numero(num):
	'''numero : NUM
			| NUM PUNTO NUM
			| MAS NUM
			| MAS NUM PUNTO NUM
			| MENOS NUM
			| MENOS NUM PUNTO NUM'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

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
	
#---------------------------------------------------------#

def p_granzeta(expr):
	'''granz : z
			| ternario'''
	
	expr[0] = expr[1]

#---------------------------------------------------------#
	
def p_zeta(expr):
	'''z : zso
		| operacion'''
	
	expr[0] = expr[1]
	
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
	
	expr[0] = expr[1]

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_vector(expr):
	'''vector : LCORCH z separavec RCORCH
			| LPAREN vector RPAREN'''			
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':	# vec -> (vec)
		expr[0] = expr[2]
	elif (tipo_segun(expr[2]) != tipo_segun(expr[3])) & (tipo_segun(expr[3]) != 'vacio'):	
		error_semantico(expr,2,"El vector debe contener elementos del mismo tipo")
	else:
		expr[0] = Vector('vector'+tipo_segun(expr[2]))
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = '[' + expr[2].impr + expr[3].impr + ']'

#---------------------------------------------------------#

def p_separavector(expr):
	'''separavec : empty
				| COMA z separavec'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2:
		expr[0] = Vector('vacio')
	elif (tipo_segun(expr[2]) != tipo_segun(expr[3])) & (tipo_segun(expr[3]) != 'vacio') :
		error_semantico(expr,2,"El vector debe contener elementos del mismo tipo")
	else:
		expr[0] = Vector(tipo_segun(expr[2]))

	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2:
		expr[0].impr = ', ' + expr[2].impr + expr[3].impr		

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_registro(expr):
	'''registro : LLLAVE RLLAVE
				| LLLAVE VAR DOSPTOS z separareg RLLAVE
				| LPAREN registro RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':	# reg -> (reg)
		expr[0] = expr[2]
	elif len(expr) == 3 : # reg -> {}
		expr[0] = Registro([],[])
	else:
		expr[0] = Registro( [expr[2]]+expr[5].campos , [tipo_segun(expr[4])]+expr[5].tipos_campos )

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
				| COMA VAR DOSPTOS z separareg'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) == 2 :
		expr[0] = Registro([],[])
	else:
		expr[0] = Registro( [expr[2]]+expr[5].campos , [tipo_segun(expr[4])]+expr[5].tipos_campos )

	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2 :
		expr[0].impr = ', ' + expr[2] + ': ' + expr[4].impr + expr[5].impr
	
#---------------------------------------------------------#
#---------------------------------------------------------#

def p_asignacion(expr):
	'''asignacion : variable operasig z
				| variable operasig ternario'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	global variables
	
	if type(expr[3]) == Variable:	# si aparece una variable del lado derecho de la asignacion
		if not(expr[3].nombre in variables):
			error_semantico(expr,3,"Opera con variable no inicializada")
		
		elif (expr[3].campo != 'None') & (type(variables[expr[3].nombre]) != dict):
			error_semantico(expr,3,"Accede a campo de variable que no es registro")
		
		elif expr[3].array_elem >= 1:
			if (expr[3].campo != 'None'):
				if variables[expr[3].nombre][expr[3].campo][:6] != 'vector':
					error_semantico(expr,3,"Accede a indice de variable que no es vector")
			elif variables[expr[3].nombre][:6] != 'vector':
				error_semantico(expr,3,"Accede a indice de variable que no es vector")
	
	tipoZ =	tipo_segun(expr[3])

	if expr[2] == '=':	# asigno una variable -> inicializo o piso su tipo
		
		if (expr[1].nombre in variables): # si la variable ya se uso antes
			if expr[1].campo != 'None': # registro.campo = bla
				if type(variables[expr[1].nombre]) != dict:	# esta cambiando de tipo a registro
					variables[expr[1].nombre] = {}
				variables[expr[1].nombre][expr[1].campo] = tipoZ

			elif expr[1].array_elem >= 1: 	# var[num] = bla
				if type(variables[expr[1].nombre]) == dict:
					variables[expr[1].nombre] = 'vector' + tipoZ
				elif variables[expr[1].nombre][:6] != 'vector':
					variables[expr[1].nombre] = 'vector' + tipoZ
				elif (variables[expr[1].nombre][:6] == 'vector') & (variables[expr[1].nombre][6:] != tipoZ): # veo que matchee el tipo de ahora
					error_semantico(expr,1,"No respeta el tipo del vector")

			else:	# es una variable cualquiera, no var[num] ni reg.campo
	
				if tipoZ == 'registro':	# reflejo los campos
					variables[expr[1].nombre] = campos_a_dic(expr[3])
				elif tipoZ == 'vreg': # reflejo los campos de la variable q es registro
					variables[expr[1].nombre] = variables[expr[3].nombre]
				else:
					variables[expr[1].nombre] = tipoZ

		else:	# declaro la variable
			
			if tipoZ == 'registro':	# reflejo los campos
				variables[expr[1].nombre] = campos_a_dic(expr[3])				
		
			elif tipoZ == 'vreg': # reflejo los campos de la variable q es registro
				variables[expr[1].nombre] = variables[expr[3].nombre]
	
			elif expr[1].array_elem >= 1:	# declaro un vector a traves de uno de sus elementos
				variables[expr[1].nombre] = 'vector' + tipoZ

			else:
				variables[expr[1].nombre] = tipoZ

	else:	# aca la variable ya deberia estar inicializada
		if not(expr[1].nombre in variables):
			error_semantico(expr,1,"Variable no inicializada")
		else:
			#tipoV = variables[expr[1].nombre]
			tipoV = tipo_segun(expr[1])

			if expr[2] == '+=': # es numerico o cadena
				if not((numericos(tipoV,tipoZ)) | ((tipoV == tipoZ) & (tipoZ == 'str'))):
					error_semantico(expr,2,"El tipo debe ser numerico o cadena")
			else: # es numerico
				if not(numericos(tipoV,tipoZ)):
					error_semantico(expr,2,"El tipo debe ser numerico")

	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr
	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#	

def p_operasig(op):
	'''operasig : IGUAL
				| MAS IGUAL
				| MENOS IGUAL
				| POR IGUAL
				| DIV IGUAL'''

	op[0] = op[1]
	if len(op) == 3:
		op[0] += op[2]
	
#---------------------------------------------------------#
#---------------------------------------------------------#
	
def p_matematico(expr):
	'''matematico : matprim operMatBinario matf
				| LPAREN matematico RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':	# mat -> (mat)
		expr[0] = expr[2]
	
	else:
		tipo1 = tipo_segun(expr[1])
		tipo2 = tipo_segun(expr[3])
		
		if expr[2] == '+':
			if not(numericos(tipo1,tipo2)) | ((tipo1 == 'str') & (tipo2 == 'str')):
				error_semantico(expr,2,"Tipos incompatibles")
				
		elif expr[2] == '%':
			if (tipo1 != 'int') & (tipo2 != 'int'):
				error_semantico(expr,2,"El tipo debe ser entero")
		
		elif not(numericos(tipo1,tipo2)):
			error_semantico(expr,2,"El tipo debe ser numerico")
		
		if (tipo1 == 'str'):
			expr[0] = Operacion('str')
		elif (tipo1 == 'float') | (tipo2 == 'float'):
			expr[0] = Operacion('float')
		else:
			expr[0] = Operacion('int')
			
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':	# mat -> (mat)
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr

#---------------------------------------------------------#

def p_matprim(expr):		   
	'''matprim : matprim operMatBinario matf
				| matf'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) == 2:
		expr[0] = expr[1]

	else:
		tipo1 = tipo_segun(expr[1])
		tipo2 = tipo_segun(expr[3])
		
		if expr[2] == '+':
			if not(numericos(tipo1,tipo2)) | ((tipo1 == 'str') & (tipo2 == 'str')):
				error_semantico(expr,2,"Tipos incompatibles")
				
		elif expr[2] == '%':
			if (tipo1 != 'int') & (tipo2 != 'int'):
				error_semantico(expr,2,"El tipo debe ser entero")
		
		elif not(numericos(tipo1,tipo2)):
			error_semantico(expr,2,"El tipo debe ser numerico")
			
		if (tipo1 == 'str'):
			expr[0] = Operacion('str')
		elif (tipo1 == 'float') | (tipo2 == 'float'):
			expr[0] = Operacion('float')
		else:
			expr[0] = Operacion('int')

	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr
	
#---------------------------------------------------------#

def p_matf(expr):
	'''matf : zso
			| LPAREN matematico RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2:
		expr[0] = expr[1]

	else:
		expr[0] = expr[2]

	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2:
		expr[0].impr = '(' + expr[2].impr + ')'

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
#---------------------------------------------------------#

def p_autoincdec(expr):
	'''autoincdec : operMatUnario variable
				| variable operMatUnario'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if (expr[1] == '++') | (expr[1] == '--') :
		if variables[expr[2].nombre] != 'int':
			error_semantico(expr,2,"El tipo debe ser entero")
	elif variables[expr[1].nombre] != 'int':
		error_semantico(expr,1,"El tipo debe ser entero")
		
	#### FORMATO PARA IMPRIMIR ####
	
	if (expr[1] == '++') | (expr[1] == '--') :
		imprimir = expr[1] + expr[2].impr
	else:
		imprimir = expr[1].impr + expr[2]
		
	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_operMatUnario(op):
	'''operMatUnario : MAS MAS
					| MENOS MENOS'''

	op[0] = op[1]
	op[0] += op[2]

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_relacion(expr):
	'''relacion : relprim operRelacion relf
			  | LPAREN relacion RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if expr[1] == '(':	# rel -> (rel)
		expr[0] = expr[2]
	
	else:
		tipoZ1 = tipo_segun(expr[1])
		tipoZ2 = tipo_segun(expr[3])
		
		if len(expr[2]) == 1: # para < y > solo numericos
			if not(numericos(tipoZ1,tipoZ2)):
				error_semantico(expr,2,"El tipo debe ser numerico")
		elif not(numericos(tipoZ1,tipoZ2) | (tipoZ1 == tipoZ2)) : # para == y != vale cualquier tipo siempre y cuando sean los dos el mismo
			error_semantico(expr,2,"Los tipos deben coincidir")
		
		expr[0] = Operacion('bool')	

	#### FORMATO PARA IMPRIMIR ####

	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr
	
#---------------------------------------------------------#

def p_relprim(expr):		   
	'''relprim : relprim operRelacion relf
				| relf'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2: 
		expr[0] = expr[1]

	else:
		tipoZ1 = tipo_segun(expr[1])
		tipoZ2 = tipo_segun(expr[3])
		
		if len(expr[2]) == 1: # para < y > solo numericos
			if not(numericos(tipoZ1,tipoZ2)):
				error_semantico(expr,2,"El tipo debe ser numerico")
		elif not(numericos(tipoZ1,tipoZ2) | (tipoZ1 == tipoZ2)) : # para == y != vale cualquier tipo siempre y cuando sean los dos el mismo
				error_semantico(expr,2,"Los tipos deben coinicidir")
		
		expr[0] = Operacion('bool')	

	#### FORMATO PARA IMPRIMIR ####

	if len(expr) > 2:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr

#---------------------------------------------------------#

def p_relf(expr):
	'''relf : zso
			| matematico
			| LPAREN relacion RPAREN
			| LPAREN logico RPAREN
			| NOT zso
			| NOT LPAREN operacion RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2: 
		expr[0] = expr[1]

	else:
		if len(expr) == 5:
			if tipo_segun(expr[3]) != 'bool':
				error_semantico(expr,3,"El tipo debe ser bool")
		elif len(expr) == 3:
			if tipo_segun(expr[1]) != 'bool':
				error_semantico(expr,2,"El tipo debe ser bool")
		
		expr[0] = Operacion('bool')	

	#### FORMATO PARA IMPRIMIR ####

	if len(expr) == 4:
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 5:
		expr[0].impr = 'NOT(' + expr[3].impr + ')'
	elif len(expr) == 3:
		expr[0].impr = 'NOT ' + expr[2].impr

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
#---------------------------------------------------------#

def p_logico(expr):
	'''logico : logprim operLogicoBinario logf
			  | LPAREN logico RPAREN
			  | NOT zso
			  | NOT LPAREN operacion RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3:	# not
		if tipo_segun(expr[2]) != 'bool':
			error_semantico(expr,2,"El tipo debe ser bool")
	elif len(expr) == 5:	# not(bla)
		if tipo_segun(expr[3]) != 'bool':
			error_semantico(expr,3,"El tipo debe ser bool")
	else:
		tipo1 = tipo_segun(expr[1])
		tipo2 = tipo_segun(expr[3])
		
		if (tipo1 != 'bool') | (tipo1 != 'bool'):
			error_semantico(expr,2,"El tipo debe ser bool")
		
	expr[0] = Operacion('bool')
	
	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 3:	# not
		expr[0].impr = 'NOT ' + expr[2].impr
	elif len(expr) == 5:	# not(bla)
		expr[0].impr = 'NOT(' + expr[3].impr + ')'
	else:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr

#---------------------------------------------------------#

def p_logprim(expr):
	'''logprim : logprim operLogicoBinario logf
				| logf'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) == 2:
		expr[0] = expr[1]
	else:
		tipo1 = tipo_segun(expr[1])
		tipo2 = tipo_segun(expr[3])
		
		if (tipo1 != 'bool') | (tipo1 != 'bool'):
			error_semantico(expr,2,"El tipo debe ser bool")
		
		expr[0] = Operacion('bool')
	
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) > 2:
		expr[0].impr = expr[1].impr + ' ' + expr[2] + ' ' + expr[3].impr

#---------------------------------------------------------#

def p_logf(expr):
	'''logf : zso
			| relacion
			| LPAREN logico RPAREN
			| NOT LPAREN operacion RPAREN
			| NOT zso'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	if len(expr) == 2: 
		expr[0] = expr[1]

	else:
		if len(expr) == 5:
			if tipo_segun(expr[3]) != 'bool':
				error_semantico(expr,3,"El tipo debe ser bool")
		elif len(expr) == 4:
			if tipo_segun(expr[2]) != 'bool':
				error_semantico(expr,2,"El tipo debe ser bool")
		elif len(expr) == 3:
			if tipo_segun(expr[2]) != 'bool':
				error_semantico(expr,2,"El tipo debe ser bool")
		
		expr[0] = Operacion('bool')	

	#### FORMATO PARA IMPRIMIR ####

	if len(expr) == 4:
		expr[0].impr = '(' + expr[2].impr + ')'
	elif len(expr) == 5:
		expr[0].impr = 'NOT(' + expr[3].impr + ')'
	elif len(expr) == 3:
		expr[0].impr = 'NOT ' + expr[2].impr

#---------------------------------------------------------#

def p_operLogBinario(op):
	'''operLogicoBinario : AND
						| OR'''

	op[0] = op[1]

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_ternario(expr):
	'''ternario : g PREG granz DOSPTOS granz
				| LPAREN ternario RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if expr[1] == '(':
		expr[0] = expr[2]
	else:
		tipoG = tipo_segun(expr[1])
		tipoZ1 = tipo_segun(expr[3])
		tipoZ2 = tipo_segun(expr[5])
		
		if (tipoG != 'bool') | (tipoZ1 != tipoZ2):
			error_semantico(expr,1,"La condicion debe ser booleana y las operaciones deben tener el mismo tipo")
		else:
			expr[0] = Operacion(tipoZ1)

	#### FORMATO PARA IMPRIMIR ####
	
	if expr[1] == '(':
		expr[0].impr = '(' + expr[2].impr + ')'
	else:
		expr[0].impr = expr[1].impr + ' ? ' + expr[3].impr + ' : ' + expr[5].impr

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_operacion(expr):
	'''operacion : matematico
				| relacion
				| logico'''

	expr[0] = expr[1]

#---------------------------------------------------------#	
#---------------------------------------------------------#	

def p_sentencia_(expr):
	'''sentencia : asignacion PTOCOMA
				| PRINT z PTOCOMA
				| autoincdec PTOCOMA'''

	#### FORMATO PARA IMPRIMIR ####

	if len(expr) == 3:
		imprimir = expr[1].impr + ';\n'
	else:
		imprimir = 'print ' + expr[2].impr + ';\n'

	expr[0] = Codigo(imprimir)
	
#---------------------------------------------------------#
#---------------------------------------------------------#

def p_funcion_multesc(expr):
	'''funcion : MULTESC LPAREN z COMA z RPAREN
				| MULTESC LPAREN z COMA z COMA z RPAREN'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	tipoZ1 = tipo_segun(expr[3])
	tipoZ2 = tipo_segun(expr[5])
	#tipoZ3 = tipo_segun(expr[7])
	
	if (tipoZ1[:6] != 'vector') | (not(numericos(tipoZ1[6:],tipoZ2))):
		error_semantico(expr,1,"multiplicacionEscalar(vector,numerico[,bool])")
	
	if len(expr) == 9:
		tipoZ3 = tipo_segun(expr[7])
		
		if tipoZ3 != 'bool':
			error_semantico(expr,1,"multiplicacionEscalar(vector,numerico[,bool])")

	if (tipoZ1[6:] == 'float') | (tipoZ2 == 'float'):
		expr[0] = Funcion('vectorfloat')
	else:
		expr[0] = Funcion('vectorint')

	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'multiplicacionEscalar(' + expr[3].impr + ', ' + expr[5].impr
	
	if len(expr) == 9:
		expr[0].impr += ', ' + expr[7].impr + ')'
	else:
		expr[0].impr += ')'
	
#---------------------------------------------------------#
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'str':
		error_semantico(expr,1,"capitalizar(cadena)")

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
		error_semantico(expr,1,"colineales(vectornumerico,vectornumerico)")
	elif (tipoZ1[-3:] != 'int') & (tipoZ1[-5:] != 'float') & (tipoZ2[-3:] != 'int') & (tipoZ2[-5:] != 'float'): # numericos
		error_semantico(expr,1,"colineales(vectornumerico,vectornumerico)")
	
	expr[0] = Funcion('bool')
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'colineales(' + expr[3].impr + ', ' + expr[5].impr + ')'

#---------------------------------------------------------#

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if (tipo_segun(expr[3]) != 'str') & (tipo_segun(expr[3])[:6] != 'vector'): 
		error_semantico(expr,1,"length(cadena o vector)")
	
	expr[0] = Funcion('int')
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0].impr = 'length(' + expr[3].impr + ')'

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_stmt(expr):
	'''stmt : closedstmt
			| openstmt'''

	expr[0] = expr[1]

#---------------------------------------------------------#

def p_closedstmt(expr):
	'''closedstmt : sentencia 
				| LLLAVE codigo RLLAVE
				| dowhile 
				| IF LPAREN g RPAREN closedstmt ELSE closedstmt
				| loopheader closedstmt
				| comentario closedstmt'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) > 4:	# if (g) bla...
		if tipo_segun(expr[3]) != 'bool':
			error_semantico(expr,3,"La guarda debe ser booleana")
	
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) == 2:
		imprimir = expr[1].impr
	elif len(expr) == 3:
		imprimir = expr[1].impr
		if (expr[1].impr)[0] == '#':
			imprimir += '\n' + expr[2].impr
		else:
			imprimir += tabular(expr[2])
	elif len(expr) == 4:
		imprimir = '{\n' + expr[2].impr + '}'
	else:
		imprimir = 'if('+ expr[3].impr + ')' + tabular(expr[5]) + 'else' + tabular(expr[7])

	expr[0] = Codigo(imprimir)
	if len(expr) == 4:
		expr[0].llaves = 1

#---------------------------------------------------------#

def p_openstmt(expr):
	'''openstmt : IF LPAREN g RPAREN stmt
				| IF LPAREN g RPAREN closedstmt ELSE openstmt
				| loopheader openstmt
				| comentario openstmt'''
	
	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if len(expr) > 3:
		if tipo_segun(expr[3]) != 'bool':
			error_semantico(expr,3,"La guarda debe ser booleana")
	
	#### FORMATO PARA IMPRIMIR ####
	
	if len(expr) == 3:
		imprimir = expr[1].impr
		if (expr[1].impr)[0] == '#':
			imprimir += '\n' + expr[2].impr
		else:
			imprimir += tabular(expr[2])
	else:
		imprimir = 'if(' + expr[3].impr + ')' + tabular(expr[5])
		if len(expr) > 6:
			imprimir += 'else' + tabular(expr[7])
	
	expr[0] = Codigo(imprimir)
	
#---------------------------------------------------------#

def p_bucle(expr):
	'''loopheader : for
				| while'''

	expr[0] = expr[1]

#---------------------------------------------------------#

def p_for_sinasig(expr):
	'''for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN
			| FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN 
			| FOR LPAREN PTOCOMA g PTOCOMA autoincdec RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####

	global variables
	
	if tipo_segun(expr[4]) != 'bool':
		error_semantico(expr,4,"La guarda debe ser booleana")

	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'for( ; ' + expr[4].impr + '; '
	
	if expr[6] == ')':
		imprimir += ')'# + expr[7].impr
	else:
		imprimir += expr[6].impr + ')'# + expr[8].impr

	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_for_conasig(expr):
	'''for : FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA autoincdec RPAREN'''

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	global variables
	
	if tipo_segun(expr[5]) != 'bool':
		error_semantico(expr,5,"La guarda debe ser booleana")

	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'for(' + expr[3].impr + ' ; ' + expr[5].impr + '; '
	
	if expr[7] == ')':
		imprimir += ')'# + expr[7].impr
	else:
		imprimir += expr[7].impr + ')'# + expr[9].impr
		
	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_while(expr):
	'while : WHILE LPAREN g RPAREN'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[3]) != 'bool':
		error_semantico(expr,3,"La guarda debe ser booleana")
		
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'while(' + expr[3].impr + ')'# + expr[5].impr
	expr[0] = Codigo(imprimir)
	
#---------------------------------------------------------#

def p_dowhile(expr):
	'dowhile : DO stmt WHILE LPAREN g RPAREN PTOCOMA'

	#### CHEQUEO Y ASIGNACION DE TIPOS ####
	
	if tipo_segun(expr[5]) != 'bool':
		error_semantico(expr,5,"La guarda debe ser booleana")

	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = 'do' + tabular(expr[2]) + 'while(' + expr[5].impr + ');\n'
	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_codigo(expr):
	'''codigo : stmt codigo
		    | stmt
		    | comentariosfinales'''
	
	#### FORMATO PARA IMPRIMIR ####
	
	imprimir = expr[1].impr
	
	if len(expr) == 3:
		imprimir += expr[2].impr
	
	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_comentario(expr):
	'comentario : COMENT'
	
	#### FORMATO PARA IMPRIMIR ####
	
	expr[0] = Codigo(expr[1])

#---------------------------------------------------------# NUEVOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

def p_comentariosfinales(expr):
	'''comentariosfinales : comentario
						| comentario comentariosfinales'''

	#### FORMATO PARA IMPRIMIR ####
 
	imprimir = expr[1].impr
	
	if len(expr) == 3:
		imprimir += '\n' + expr[2].impr + '\n'

	expr[0] = Codigo(imprimir)

#---------------------------------------------------------#

def p_empty(p):
	'empty :'
	pass

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_error(expr):
	#print expr
	message = "[Syntax error]"
	message += "\nline:" + str(expr.lineno)
	message += "\nindex:" + str(expr.lexpos)
	raise Exception(message)
    
#---------------------------------------------------------#

def error_semantico(expr,n,msg):
	message = "[Semantic error]"
	message += "\n"+msg
	message += "\nline:" + str(expr.lineno(n))
	message += "\nindex:" + str(expr.lexpos(n))
	raise Exception(message)

#---------------------------------------------------------#
#---------------------------------------------------------#

def numericos(tipo1,tipo2):

	return (tipo1 in ['int','float']) & (tipo2 in ['int','float'])

#---------------------------------------------------------#

def tipo_segun(objeto):

	global variables
	
	if type(objeto) == Variable:
		if objeto.array_elem >= 1:	# es una posicion de un arreglo
			if objeto.campo != 'None':	# es algo tipo reg.campo
				variable = variables[objeto.nombre][objeto.campo][6:]
			else:
				variable = variables[objeto.nombre][6:]
			for x in range(1,objeto.array_elem):
				variable = variable[6:]
								
		elif objeto.campo != 'None':	# es algo tipo reg.campo
			variable = (variables[objeto.nombre])[objeto.campo]
		elif type(variables[objeto.nombre]) == dict:
			variable = 'vreg'
		else:		
			variable = variables[objeto.nombre]
	else:
		variable = objeto.tipo
		
	return variable

#---------------------------------------------------------#

def campos_a_dic(reg):
	
	dic = {}
	
	for x in range(0,len(reg.campos)):
		dic[reg.campos[x]] =  reg.tipos_campos[x]
		
	return dic

#---------------------------------------------------------#
#---------------------------------------------------------#

def tabular(codigo):
	
	lineas = (codigo.impr).splitlines()
	
	if codigo.llaves == 1:
		res = "{\n"	
		for l in lineas[1:-1]:
			#if l[0] == '{':
				#res += l + '\n'
			#elif l[0] == '}':
				#res += l + '\n'
			#else:
			res += '\t' + l + '\n'
		res += '}\n'
	else:
		res = "\n"	
		for l in lineas:
			res += '\t' + l + '\n'
		
	return res
