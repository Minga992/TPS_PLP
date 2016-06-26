from lexer_rules import tokens

from expressions import *

# diccionario de variables, nombre:tipo
variables = {}

def p_inicial(expr):
	'start : codigo'
	expr[0] = expr[1] # ver esto, ACA Y EN LOS SIGUENTES

def p_constante_valor(cte):
	'constante : STR'
	'		   | BOOL'
	'		   | numero'
	'		   | LPAREN constante RPAREN'
	#'		   | funcion'
	
	if cte[1] == '(':
		cte[0] = cte[2]
	else:	
		cte[0] = Constante(cte[1],type(cte[1]))
		

def p_constante_funcion(f):
	'constante : funcion'
	
	#cte[0] = Constante()  STAND BY


def p_variable(expr):
	'variable : VAR'
	'		  | VAR PUNTO VAR'
	'		  | VAR LCORCH NUM RCORCH'
	'		  | LPAREN variable RPAREN'

	if expr[1] == '(':
		expr[2] = expr[0]
	elif len(expr) == 2:
		variables[expr[1]] = expr[0].tipo
	elif len(expr) == 4:
		variables[expr[1]] = 'registro'	# ver que pasa con el campo
	else:
		if expr[1] in variables:
			if variables[expr[1]] != 'vector'+expr[0].tipo:
				raise SyntaxError
		else:
			variables[expr[1]] = 'vector'+expr[0].tipo
		
	
def p_numero(num):
	'numero : NUM'
	'		| NUM PUNTO NUM'
	'		| MAS NUM'
	'		| MENOS NUM'
	'		| MAS NUM PUNTO NUM'
	'		| MENOS NUM PUNTO NUM'
	
	if num[1] == '+':
		if len(num) == 3:
			num[0] = Numero(+num[2],int)
		else:
			num[0] = Numero(float('+'+str(num[2])+'.'+str(num[4])),float)
	elif num[1] == '-':
		if len(num) == 3:
			num[0] = Numero(-num[2],int)
		else:
			num[0] = Numero(float('-'+str(num[2])+'.'+str(num[4])),float)
	else:
		if len(num) == 2:
			num[0] = Numero(num[2],int)
		else:
			num[0] = Numero(float(str(num[2])+'.'+str(num[4])),float)
	
	
def p_zeta(expr):
	'z : variable'
	'  | constante'
	'  | vector'
	'  | registro'
	'  | operacion'
	
	expr[0] = expr[1]
	
	
def p_ge(expr):
	'g : variable'
	'  | constante' 
	'  | relacion'
	'  | logico'
	
	expr[0] = expr[1]


def p_vector(expr):
	'vector : LCORCH constante separavec RCORCH'
	'		| LCORCH vector separavec RCORCH'
	'		| LCORCH registro separavec RCORCH'
	'		| LPAREN vector RPAREN'
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif (expr[2].tipo != expr[3].tipo) & expr[3] != 'vacio' :
		raise SyntaxError
	else:
		expr[0] = Vector(expr[2].tipo)


def p_separavector(expr):
	'separaVec : empty'
	'		   | constante separavec'
	'		   | vector separavec'
	'		   | registro separavec'

	if len(expr) == 2:
		expr[0] = SepVec('vacio')
	elif (expr[1].tipo != expr[2].tipo) & expr[2] != 'vacio' :
		raise SyntaxError
	else:
		expr[0] = SepVec(expr[1].tipo)


def p_registro(expr):
	'registro : LLLAVE RLLAVE'
	'		  | LLLAVE VAR DOSPTOS constante separareg RLLAVE'
	'		  | LLLAVE VAR DOSPTOS vector separareg RLLAVE'
	'		  | LLLAVE VAR DOSPTOS registro separareg RLLAVE'
	'		  | LPAREN registro RPAREN'
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3 : 
		expr[0] = Registro([],[])
	else:
		expr[0] = Registro([expr[2].nombre]+expr[5].campos,[expr[2].tipo]+expr[5].tipos)
		

def p_separaregistro(expr):
	'separaReg : empty'
	'		   | COMA VAR DOSPTOS constante separareg'
	'		   | COMA VAR DOSPTOS vector separareg'
	'		   | COMA VAR DOSPTOS registro separareg'
	
	if len(expr) == 2 :
		expr[0] = Registro([],[])
	else:
		expr[0] = Registro([expr[4].nombre]+expr[5].campos,[expr[4].tipo]+expr[5].tipos)
	

def p_asignacion(expr):
	'asignacion : variable operasig z'
	'			| variable operasig ternario'
	
	expr[1] = Variable(expr[3].tipo)
	

def p_operasig(op):
	'operAsig : IGUAL'
	'		  | MAS IGUAL'
	'		  | MENOS IGUAL'
	'		  | POR IGUAL'
	'		  | DIV IGUAL'


def p_matematico(expr):
	'matematico : z operMatBinario z'
	'			| operMatUnario var'
	'			| var operMatUnario'

	if len(expr) == 4:
		if expr[1].tipo != expr[3].tipo: # falta poner q es solo para numericos y string en el caso de +
			raise SyntaxError
		else:
			expr[0] = Constante(5,expr[1].tipo)
	else:
		if (expr[1].tipo != 'int') | (expr[2].tipo != 'int')	# agregar lo que va en expr 0
			raise SyntaxError


def p_operMatBinario(op):
	'operMatBinario : MAS'
	'				| MENOS'
	'				| POR'
	'				| POT'
	'				| MOD'
	'				| DIV'


def p_operMatUnario(op):
	'operMatUnario : MAS MAS'
	'			   | MENOS MENOS'


def p_relacion(expr):
	'relacion : z operRealacion z'
	'		  | LPAREN relacion RPAREN'

	if expr[1] == '(':
		expr[0] = expr[2]
	elif expr[1].tipo != expr[3].tipo:	# ojo, hay que ver si hay tipos para los que estos operadores no esten definidos
		raise SyntaxError
	else:
		expr[0] = Constante(True,'bool')	# ojo con este valor


def p_operRelacion(op):
	'operRelacion : IGUAL IGUAL'
	'			  | ADM IGUAL'
	'			  | MAYOR'
	'			  | MENOR'


def p_logico(expr):
	'logico : z operLogicoBinario z'
	'		| NOT z'
	'		| LPAREN logico RPAREN'
	
	if expr[1] == '(':
		expr[0] = expr[2]
	elif len(expr) == 3:
		if expr[2].tipo != 'bool':
			raise SyntaxError
	elif (expr[1].tipo != 'bool') & (expr[3].tipo != 'bool'):
		raise SyntaxError
	else:
		expr[0] = Constante(True,'bool')	# ojo con este valor
	

def p_operLogBinario(op):
	'operLogBinario : AND'
	'				| OR'


def p_ternario(expr):
	'ternario : LPAREN constante RPAREN PREG z DOSPTOS z'
	'		  | LPAREN constante RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN relacion RPAREN PREG z DOSPTOS z'
	'		  | LPAREN relacion RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN logico RPAREN PREG z DOSPTOS z'
	'		  | LPAREN logico RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN variable RPAREN PREG z DOSPTOS z'
	'		  | LPAREN variable RPAREN PREG ternario DOSPTOS ternario'
	
	if expr[2].tipo != 'bool' | (expr[5].tipo != expr[7].tipo):
		raise SyntaxError
	else:
		expr[0] = Ternario(expr[5].tipo)
	

def p_operacion(expr):
	'operacion : matematico'
	'		   | relacion'
	'		   | logico'
	
	expr[0] = expr[1]
	
	
def p_sentencia_stipo(expr):
	'sentencia : asignacion PTOCOMA'
	'		   | PRINT z PTOCOMA'


def p_sentencia_ctipo(expr):
	'sentencia : operMatUnario variable PTOCOMA'
	'		   | variable operMatUnario PTOCOMA'
	
	if (expr[1].tipo != 'int') | (expr[2].tipo != 'int'):
		raise SyntaxError
	

def p_bloque(expr):
	'bloque : LLLAVE codigo RLLAVE'
	'		| sentencia '
	'		| condicional'
	'		| bucle'
	
	
def p_funcion_multesc(expr):
	'funcion : MULTESC LPAREN z COMA z RPAREN'
	'		 | MULTESC LPAREN z COMA z COMA z RPAREN'
	
	if (expr[3].tipo != 'vectorint') | (expr[3].tipo != 'vectorfloat') | (expr[5].tipo != 'int') | (expr[5].tipo != 'float'):
		raise SyntaxError
	if len(expr) == 9:
		if expr[7].tipo != 'bool':
			raise SyntaxError
	if (expr[3].tipo == 'vectorfloat') | (expr[5].tipo == 'float'):
		expr[0] = Funcion('vectorfloat')
	else:
		expr[0] = Funcion('vectorint')
	
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	
	if expr[3].tipo != 'str':
		raise SyntaxError
	expr[0] = Funcion('str')
	
	
def p_funcion_colin(expr):
	'funcion : COLIN LPAREN z COMA z RPAREN'
	
	if (expr[3].tipo != 'vectorint') | (expr[3].tipo != 'vectorfloat') | (expr[5].tipo != 'vectorint') | (expr[5].tipo != 'vectorfloat'):
		raise SyntaxError
	expr[0] = Funcion('bool')
	

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'
	
	if (expr[3].tipo != 'vector') | (expr[3].tipo != 'str'):  # ojo q vale vector de lo q sea
		raise SyntaxError
	expr[0] = Funcion('int')


def p_condicional(expr):
	'condicional : IF LPAREN g RPAREN bloque'
	'			 | IF LPAREN g RPAREN bloque ELSE bloque'
	
	if expr[3].tipo != 'bool':
		raise SyntaxError
	

def p_bucle(expr):
	'bucle : for'
	'	   | while'
	'	   | dowhile'


def p_for(expr):
	'for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA operMatUnario var RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA var operMatUnario RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA operMatUnario var RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA var operMatUnario RPAREN bloque'

	# es ver si g es bool. probablemente haya que hacer varios casos


def p_while(expr):
	'while : WHILE LPAREN g RPAREN bloque'

	if expr[3].tipo != 'bool':
		raise SyntaxError	


def p_dowhile(expr):
	'dowhile : DO bloque WHILE LPAREN g RPAREN PTOCOMA'

	if expr[5].tipo != 'bool':
		raise SyntaxError


def p_codigo(expr):
	'codigo : bucle codigo'
	'	    | condicional codigo'
	' 	    | sentencia codigo'
	'	    | bucle' 
	'	    | condicional' 
	'	    | sentencia' 


def p_comentario(expr):
	'comentario : COMENT'

def p_empty(p):
	'empty :'
    pass

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
