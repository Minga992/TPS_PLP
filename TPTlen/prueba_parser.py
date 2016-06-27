import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)

#text = "inicio = \"Hola\";\ni =0;\ndo{ i++;\ninicio += \" \";\n}while (j % 32 != 0); print (\"Mundo!\");"
#text = "inicio = \"Hola\";\nj = length(inicio);"
text = "inicio = \"Hola\";\n"
#text += "i =0;\n"
#text += "do{ i++;\n"
#text += "inicio += \" \"; \n"
#text += "j = length(inicio);\n"
#text += "}while (j != 0); print (\"Mundo!\");"
ast = parser.parse(text, lexer)

#result = ast.evaluate()
#print result
