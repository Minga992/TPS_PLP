import lexer_rules
import parser_rules

from sys import argv, exit

from ply.lex import lex
from ply.yacc import yacc


if __name__ == "__main__":
	
    #if len(argv) < 4:
        #print "Invalid arguments."
        #print "Use:"
        #print "  SLSParser [-o SALIDA] [-c ENTRADA | FUENTE]"
        #exit()
#
	#if len(argv) == 4:	# viene con FUENTE
		#text = argv[3]
	#else:	# viene con -c ENTRADA
		#text = arg

    text = argv[1]

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    expression = parser.parse(text, lexer)

    result = expression.imprimir()
    print result
    
