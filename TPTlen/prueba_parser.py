import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)

#text = "inicio = \"Hola\";\ni =0;\ndo{ i++;\ninicio += \" \";\n}while (j % 32 != 0); print (\"Mundo!\");"
#text = "inicio = \"Hola\";\nj = length(inicio);"
#text = "x = (1<2)?\"si\":\"no\";"
#text += "x = capitalizar(inicio);"
#text += "i =0;\n"
#text += "do{ i++;\n"
#text += "inicio += \" \"; \n"
#text += "j = length(inicio)*i;\n"
#text += "}while (j % 32 != 0); print (\"Mundo!\");"

#probando parentesis
#text = "(((parentesis))) = (((5)*4)+(((6*6)))) + 8;"

#if con cosas turbias
#text = "if (\"\" == \"\" ) a = 3 + 4; else b = 4+3; a= b + 5 ;"
#text = "a=3; a = a + 3;"

#hago faltar cosas, cambio cosas en el medio, y los tipos lo soportan
#text = "a = true; b=5; for (;a;b++) if( a ) {b=a; if (b) b=a;} else c = 8;"
#text = " a= true ;b=a; if (b) b=a;"
#text = "a = true; b=5; for (;a;++b) b=b;"
#text = "a=1; a++;for (;true;) a=5;"
#text = "a=1; a++;"

#con esto probemos errores
#text = "a=3; a++; a--; a += 6; a -= 5; a *= 3; print (length( \"pelado\")); b= (a==8); if (b) a= a; c = a==8? a:a;"
#text = "a = 3;b= (a==8); if (b) a= a; c = a==8? a:a;"
#text = "a = 3==3.4"

#vectores
#text = "b= [3,4,5] ; b[6] = 3; a = 2 + b[4];"
text = "b[2] = 3; a= b; c = (a[4] + b[1]) ^ b[8]; a = true; d = a[3];"# if (a) then e = 5;"


#registro
#text = "a = {}; a.campo= 3; b = a.campo + 4;"

ast = parser.parse(text, lexer)

#result = ast.evaluate()
#print result
