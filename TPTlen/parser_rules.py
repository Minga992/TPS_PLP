from lexer_rules import tokens

from expressions import *

def p_expression_cte(subexpr):
	'constante : NUM'
	subexpr[0] = subexpr[1]
