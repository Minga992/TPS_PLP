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


#---------------------------------------------------------#
	
def p_constante_funcion(f):
	'constante : funcion'
	

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_variable(expr):
	'''variable : VAR
				| RES
				| VAR LCORCH z RCORCH
				| LPAREN variable RPAREN
				| VAR PUNTO VAR'''
	

#---------------------------------------------------------#
#---------------------------------------------------------#
	
def p_numero(num):
	'''numero : NUM
			| NUM PUNTO NUM
			| MAS NUM
			| MAS NUM PUNTO NUM
			| MENOS NUM
			| MENOS NUM PUNTO NUM'''
	
	
#---------------------------------------------------------#
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
	

#---------------------------------------------------------#

def p_separavector(expr):
	'''separavec : empty
				| COMA z separavec'''


#---------------------------------------------------------#
#---------------------------------------------------------#

def p_registro(expr):
	'''registro : LLLAVE RLLAVE
				| LLLAVE VAR DOSPTOS z separareg RLLAVE
				| LPAREN registro RPAREN'''


#---------------------------------------------------------#

def p_separaregistro(expr):
	'''separareg : empty
				| COMA VAR DOSPTOS z separareg'''
	
	
#---------------------------------------------------------#
#---------------------------------------------------------#

def p_asignacion(expr):
	'''asignacion : variable operasig z
				| variable operasig ternario'''
	

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


#---------------------------------------------------------#

def p_matprim(expr):		   
	'''matprim : matprim operMatBinario matf
				| matf'''

	
#---------------------------------------------------------#

def p_matf(expr):
	'''matf : zso
			| LPAREN matematico RPAREN'''


#---------------------------------------------------------#

def p_operMatBinario(op):
	'''operMatBinario : MAS
					| MENOS
					| POR
					| POT
					| MOD
					| DIV'''


#---------------------------------------------------------#
#---------------------------------------------------------#

def p_autoincdec(expr):
	'''autoincdec : operMatUnario variable
				| variable operMatUnario'''


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

	
#---------------------------------------------------------#

def p_relprim(expr):		   
	'''relprim : relprim operRelacion relf
				| relf'''


#---------------------------------------------------------#

def p_relf(expr):
	'''relf : zso
			| matematico
			| LPAREN relacion RPAREN
			| LPAREN logico RPAREN'''


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
			  | NOT z'''


#---------------------------------------------------------#

def p_logprim(expr):
	'''logprim : logprim operLogicoBinario logf
				| logf'''
	

#---------------------------------------------------------#

def p_logf(expr):
	'''logf : zso
			| relacion
			| LPAREN logico RPAREN'''


#---------------------------------------------------------#

def p_operLogBinario(op):
	'''operLogicoBinario : AND
						| OR'''

	op[0] = op[1]

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_ternario(expr):
	'''ternario : g PREG z DOSPTOS z
				| g PREG ternario DOSPTOS ternario'''


#---------------------------------------------------------#
#---------------------------------------------------------#

def p_operacion(expr):
	'''operacion : matematico
				| relacion
				| logico'''


#---------------------------------------------------------#	
#---------------------------------------------------------#	

def p_sentencia_(expr):
	'''sentencia : asignacion PTOCOMA
				| PRINT z PTOCOMA
				| autoincdec PTOCOMA'''

	
#---------------------------------------------------------#
#---------------------------------------------------------#

def p_funcion_multesc(expr):
	'''funcion : MULTESC LPAREN z COMA z RPAREN
				| MULTESC LPAREN z COMA z COMA z RPAREN'''
	
	
#---------------------------------------------------------#
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	
	
#---------------------------------------------------------#

def p_funcion_colin(expr):
	'funcion : COLIN LPAREN z COMA z RPAREN'
	

#---------------------------------------------------------#

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'
	

#---------------------------------------------------------#
#---------------------------------------------------------#

def p_stmt(expr):
	'''stmt : closedstmt
			| openstmt'''


#---------------------------------------------------------#

def p_closedstmt(expr):
	'''closedstmt : sentencia 
				| LLLAVE codigo RLLAVE
				| dowhile 
				| IF LPAREN g RPAREN closedstmt ELSE closedstmt
				| loopheader closedstmt
				| comentario closedstmt'''


#---------------------------------------------------------#

def p_openstmt(expr):
	'''openstmt : IF LPAREN g RPAREN stmt
				| IF LPAREN g RPAREN closedstmt ELSE openstmt
				| loopheader openstmt
				| comentario openstmt'''
	
	
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


#---------------------------------------------------------#

def p_for_conasig(expr):
	'''for : FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN
			| FOR LPAREN asignacion PTOCOMA g PTOCOMA autoincdec RPAREN'''


#---------------------------------------------------------#

def p_while(expr):
	'while : WHILE LPAREN g RPAREN'

	
#---------------------------------------------------------#

def p_dowhile(expr):
	'dowhile : DO stmt WHILE LPAREN g RPAREN PTOCOMA'


#---------------------------------------------------------#

def p_codigo(expr):
	'''codigo : stmt codigo
		    | stmt
		    | comentario'''
	

#---------------------------------------------------------#

def p_comentario(expr):
	'comentario : COMENT'
	

#---------------------------------------------------------#

def p_empty(p):
	'empty :'
	pass