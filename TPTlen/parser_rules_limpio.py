from lexer_rules import tokens

from expressions import *



def p_inicial(expr):
	'start : codigo'

def p_constante_valor(cte):
	'''constante : STR	
				| BOOL
				| numero
				| LPAREN constante RPAREN'''
	
def p_constante_funcion(f):
	'constante : funcion'
	
def p_variable(expr):
	'''variable : VAR
				| RES
				| VAR LCORCH NUM RCORCH
				| LPAREN variable RPAREN
				| VAR PUNTO VAR'''
	
	
def p_numero(num):
	'''numero : NUM
			| NUM PUNTO NUM
			| MAS NUM
			| MAS NUM PUNTO NUM
			| MENOS NUM
			| MENOS NUM PUNTO NUM'''
	
	
def p_zeta(expr):
	'''z : zso
		| operacion'''
	

def p_zeta_sin_oper(expr):
	'''zso : variable
			| constante
			| vector
			| registro'''
			
def p_ge(expr):
	'''g : variable
		| constante 
		| relacion
		| logico'''
	

def p_vector(expr):
	'''vector : LCORCH constante separavec RCORCH
			| LCORCH vector separavec RCORCH
			| LCORCH registro separavec RCORCH
			| LPAREN vector RPAREN'''			
	
def p_separavector(expr):
	'''separavec : empty
				| COMA constante separavec
				| COMA vector separavec
				| COMA registro separavec'''


def p_registro(expr):
	'''registro : LLLAVE RLLAVE
				| LLLAVE VAR DOSPTOS constante separareg RLLAVE
				| LLLAVE VAR DOSPTOS vector separareg RLLAVE
				| LLLAVE VAR DOSPTOS registro separareg RLLAVE
				| LPAREN registro RPAREN'''
				

def p_separaregistro(expr):
	'''separareg : empty
				| COMA VAR DOSPTOS constante separareg
				| COMA VAR DOSPTOS vector separareg
				| COMA VAR DOSPTOS registro separareg'''
	
def p_asignacion(expr):
	'''asignacion : variable operasig z
				| variable operasig ternario'''
	

def p_operasig(op):
	'''operasig : IGUAL
				| MAS IGUAL
				| MENOS IGUAL
				| POR IGUAL
				| DIV IGUAL'''
					

def p_matematico(expr):
	'''matematico : z operMatBinario zso
				| z operMatBinario LPAREN matematico RPAREN
				| LPAREN matematico RPAREN'''

def p_operMatBinario(op):
	'''operMatBinario : MAS
					| MENOS
					| POR
					| POT
					| MOD
					| DIV'''

def p_operMatUnario(op):
	'''operMatUnario : MAS MAS
					| MENOS MENOS'''

def p_relacion(expr):
	'''relacion : z operRelacion zso
				| z operRelacion LPAREN operacion RPAREN
				| LPAREN relacion RPAREN'''
			  
def p_operRelacion(op):
	'''operRelacion : IGUAL IGUAL
					| ADM IGUAL
					| MAYOR
					| MENOR'''
					

def p_logico(expr):
	'''logico : z operLogicoBinario zso
			| z operLogicoBinario LPAREN operacion RPAREN
			| NOT z
			| LPAREN logico RPAREN'''
			

def p_operLogBinario(op):
	'''operLogicoBinario : AND
						| OR'''

def p_ternario(expr):
	'''ternario : g PREG z DOSPTOS z
				| g PREG ternario DOSPTOS ternario'''
				

def p_operacion(expr):
	'''operacion : matematico
				| relacion
				| logico'''
	
def p_autoincdec(expr):
	'''autoincdec : operMatUnario variable
				| variable operMatUnario'''

def p_sentencia_(expr):
	'''sentencia : asignacion PTOCOMA
				| PRINT z PTOCOMA
				| autoincdec PTOCOMA'''






def p_funcion_multesc(expr):
	'''funcion : MULTESC LPAREN z COMA z RPAREN
				| MULTESC LPAREN z COMA z COMA z RPAREN'''
	
def p_funcion_cap(expr):
	'funcion : CAP LPAREN z RPAREN'
	

def p_funcion_colin(expr):
	'funcion : COLIN LPAREN z COMA z RPAREN'
	

def p_funcion_length(expr):
	'funcion : LENGTH LPAREN z RPAREN'

#-----------------------------------------------------------------------	


def p_bloquescond(expr):
	'''bloquescond : LLLAVE codigo RLLAVE
			| sentencia 
			| bucle'''


def p_bloque(expr):
	'''bloque : matchedstmt
				| openstmt'''
					
def p_matchedstmt(expr):
	'''matchedstmt : IF LPAREN g RPAREN matchedstmt ELSE matchedstmt
					| bloquescond'''
					
def p_openstmt(expr):
	'''openstmt : IF LPAREN g RPAREN bloque
				| IF LPAREN g RPAREN matchedstmt ELSE openstmt'''
	

#-------------------------------------------------------------------------	

def p_bucle(expr):
	#'''bucle : for'''
			#| while
			#| dowhile'''
	'bucle : dowhile'
			
#def p_for_sinasig(expr):
	#'''for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN bloque
			#| FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN bloque
			#| FOR LPAREN PTOCOMA g PTOCOMA autoincdec RPAREN bloque'''

#def p_for_conasig(expr):
	#'''for : FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN bloque
			#| FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN bloque
			#| FOR LPAREN asignacion PTOCOMA g PTOCOMA autoincdec RPAREN bloque'''

#def p_while(expr):
	#'while : WHILE LPAREN g RPAREN bloque'


def p_dowhile(expr):
	'dowhile : DO bloque WHILE LPAREN g RPAREN PTOCOMA'

def p_codigo(expr):
	'''codigo : bloque codigo
	 	    | comentario codigo
		    | bloque
		    | comentario'''


def p_comentario(expr):
	'comentario : COMENT'
	

def p_empty(p):
	'empty :'
	pass


