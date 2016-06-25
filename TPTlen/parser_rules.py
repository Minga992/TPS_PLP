from lexer_rules import tokens

from expressions import *

def p_expression_inicial(subexpr):
	'start : bucle' | 'start : condicional' | 'start : sentencia'
	subexpr[0] = subexpr[1] # ver esto, ACA Y EN LOS SIGUENTES

def p_expression_cte(subexpr):
	'constante : STR' | 'constante : BOOL' | 'constante : numero' | 'constante : LPAREN constante RPAREN' | 'constante : funcion'
	#subexpr[0]

def p_expression_var(subexpr):
	'variable : VAR' | 'variable : VAR PUNTO VAR' | 'variable : VAR LCORCH NUM RCORCH'
	#subexpr[0]	

def p_expression_num(subexpr):
	'numero : NUM' | 'numero : NUM PUNTO NUM' | 'numero : MAS NUM' | 'numero : MENOS NUM' | 'numero : MAS NUM PUNTO NUM' | 'numero : MENOS NUM PUNTO NUM'
	#subexpr[0]
	
def p_expression_z(subexpr):
	'z : varable' | 'z : constante' | 'z : vector' | 'z : registro' | 'z : operacion'
	#subexpr[0]
	
def p_expression_g(subexpr):
	'g : variable' | 'g : constante' | 'g : relacion' | 'g : logico'
	#subexpr[0]

def p_expression_vec(subexpr):
	'vector : LCORCH RCORCH' | 'vector : LCORCH constante separavec RCORCH' |  'vector : LCORCH vector separavec RCORCH' |  'vec : LCORCH registro separavec RCORCH' |  'vec : LPAREN vec RPAREN'
	#subexpr[0]

def p_expression_sepv(subexpr):
	'separavec : LAMBDA???' | 'separavec : constante separavec' | 'separavec : vector separavec' | 'separavec : registro separavec'
	#subexpr[0]

def p_expression_reg(subexpr):
	'registro : LLLAVE VAR DOSPTOS constante separareg RLLAVE' | 'reg : LLLAVE VAR DOSPTOS vector separareg RLLAVE' | 'registro : LLLAVE VAR DOSPTOS registro separareg RLLAVE' | 'reg : LPAREN registro RPAREN'
	#subexpr[0]

def p_expression_sepr(subexpr):
	'separareg : LAMBDAA???' | 'separareg : COMA VAR DOSPTOS constante separareg' | 'separareg : COMA VAR DOSPTOS vector separareg' | 'separareg : COMA VAR DOSPTOS registro separareg'
