import lexer_rules

from ply.lex import lex

#text = "# Este programa funciona bien \n"
#text += "a=100;\n"
#text += "for (i=1; i<a;i++) b = b+10*i; \n"
#text += "#Aqui se devuelve el resultado esperado\n"
#text += "res = b * 0.8;"
#text = "LALLALALAL\npepe\n999$"
text = "inicio = \"Hola\";\ni =0;\ndo{ i++;\ninicio += \" \"; \# Se agrega un espacio\nj = length(inicio) * i;\n}while (j % 32 != 0); print (\"Mundo!\");"
lexer = lex(module=lexer_rules)
lexer.input(text)

token = lexer.token()

while token is not None:
	print token
	token = lexer.token()
