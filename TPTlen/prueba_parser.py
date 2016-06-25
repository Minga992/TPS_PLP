import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)

text = "true"
ast = parser.parse(text, lexer)

result = ast.evaluate()
print result
