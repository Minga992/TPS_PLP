from lexer_rules import tokens

from expressions import *

def p_expression_inicial(subexpr):
	'start : codigo'
	subexpr[0] = subexpr[1] # ver esto, ACA Y EN LOS SIGUENTES

def p_expression_cte(subexpr):
	'constante : STR'
	'		   | BOOL'
	'		   | numero'
	'		   | LPAREN constante RPAREN'
	'		   | funcion'
	#subexpr[0]

def p_expression_var(subexpr):
	'variable : VAR'
	'		  | VAR PUNTO VAR'
	'		  | VAR LCORCH NUM RCORCH'
	'		  | LCORCH variable RCORCH'
	#subexpr[0]	

def p_expression_num(subexpr):
	'numero : NUM'
	'		| NUM PUNTO NUM'
	'		| MAS NUM'
	'		| MENOS NUM'
	'		| MAS NUM PUNTO NUM'
	'		| MENOS NUM PUNTO NUM'
	#subexpr[0]
	
def p_expression_z(subexpr):
	'z : varable'
	'  | constante'
	'  | vector'
	'  | registro'
	'  | operacion'
	#subexpr[0]
	
def p_expression_g(subexpr):
	'g : variable'
	'  | constante' 
	'  | relacion'
	'  | logico'
	#subexpr[0]

def p_expression_vec(subexpr):
	'vector : LCORCH RCORCH'
	'		| LCORCH constante separavec RCORCH'
	'		| LCORCH vector separavec RCORCH'
	'		| LCORCH registro separavec RCORCH'
	'		| LPAREN vec RPAREN'
	#subexpr[0]

def p_expression_sepv(subexpr):
	'separaVec : LAMBDA???'
	'		   | constante separavec'
	'		   | vector separavec'
	'		   | registro separavec'
	#subexpr[0]

def p_expression_reg(subexpr):
	'registro : LLLAVE VAR DOSPTOS constante separareg RLLAVE'
	'		  | LLLAVE VAR DOSPTOS vector separareg RLLAVE'
	'		  | LLLAVE VAR DOSPTOS registro separareg RLLAVE'
	'		  | LPAREN registro RPAREN'
	#subexpr[0]

def p_expression_sepr(subexpr):
	'separaReg : LAMBDAA???'
	'		   | COMA VAR DOSPTOS constante separareg'
	'		   | COMA VAR DOSPTOS vector separareg'
	'		   | COMA VAR DOSPTOS registro separareg'

def p_expression_asignacion(subexpr):
	'asignacion : variable operasig z'
	'			| variable operasig ternario'

def p_expression_operasig(subexpr):
	'operAsig : IGUAL'
	'		  | MAS IGUAL'
	'		  | MENOS IGUAL'
	'		  | POR IGUAL'
	'		  | DIV IGUAL'

def p_expression_matematico(subexpr):
	'matematico : z operMatBinario z'
	'			| operMatUnario var'
	'			| var operMatUnario'


def p_expression_operMatBinario(subexpr):
	'operMatBinario : MAS'
	'				| MENOS'
	'				| POR'
	'				| POT'
	'				| MOD'
	'				| DIV'

def p_expression_operMatUnario(subexpr):
	'operMatUnario : MAS MAS'
	'			   | MENOS MENOS'

def p_expression_relacion(subexpr):
	'relacion : z operRealacion z'
	'		  | LPAREN relacion RPAREN'

def p_expression_operRelacion(subexpr):
	'operRelacion : IGUAL IGUAL'
	'			  | ADM IGUAL'
	'			  | MAYOR'
	'			  | MENOR'

def p_expression_logico(subexpr):
	'logico : z operLogicoBinario z'
	'		| NOT z'
	'		| LPAREN logico RPAREN'
	

def p_expression_operLogBinario(subexpr):
	'operLogBinario : AND'
	'				| OR'

def p_expression_ternario(subexpr):
	'ternario : LPAREN constante RPAREN PREG z DOSPTOS z'
	'		  | LPAREN constante RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN relacion RPAREN PREG z DOSPTOS z'
	'		  | LPAREN relacion RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN logico RPAREN PREG z DOSPTOS z'
	'		  | LPAREN logico RPAREN PREG ternario DOSPTOS ternario'
	'		  | LPAREN variable RPAREN PREG z DOSPTOS z'
	'		  | LPAREN variable RPAREN PREG ternario DOSPTOS ternario'

def p_expression_operacion(subexpr):
	'operacion : matematico'
	'		   | relacion'
	'		   | logico'
	
def p_expression_sentencia(subexpr):
	'sentencia : asignacion PTOCOMA'
	'		   | operMatUnario variable PTOCOMA'
	'		   | variable operMatUnario PTOCOMA'
	'		   | PRINT z PTOCOMA'

def p_expression_bloque(subexpr):
	'bloque : codigo'
	'		| sentencia '
	'		| condicional'
	'		| bucle'
	
def p_expression_funcion(subexpr):
	'funcion : MULTESC LPAREN z COMA z RPAREN'
	'		 | MULTESC LPAREN z COMA z COMA z RPAREN'
	'		 | CAP LPAREN z RPAREN'
	'		 | COLIN LPAREN z COMA z RPAREN'
	'		 | LENGTH LPAREN z RPAREN'

def p_expression_condicional(subexpr):
	'condicional : IF LPAREN g RPAREN bloque'
	'			 | IF LPAREN g RPAREN bloque ELSE bloque'

def p_expression_bucle(subexpr):
	'bucle : for'
	'	   | while'
	'	   | dowhile'

def p_expression_for(subexpr):
	'for : FOR LPAREN PTOCOMA g PTOCOMA RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA asignacion RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA operMatUnario var RPAREN bloque'
	'	 | FOR LPAREN PTOCOMA g PTOCOMA var operMatUnario RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA asignacion RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA operMatUnario var RPAREN bloque'
	'	 | FOR LPAREN asignacion PTOCOMA g PTOCOMA var operMatUnario RPAREN bloque'

def p_expression_while(subexpr):
	'while : WHILE LPAREN g RPAREN bloque'

def p_expression_dowhile(subexpr):
	'dowhile : DO bloque WHILE LPAREN g RPAREN PTOCOMA'

def p_expression_codigo(subexpr):
	'codigo : bucle start'
	'	    | condicional start'
	' 	    | sentencia start'
	'	    | bucle' 
	'	    | condicional' 
	'	    | sentencia' 


def p_expression_comentario(subexpr):
	'comentario : COMENT'

