import lexer_rules

from ply.lex import lex

#text = "# Este programa funciona bien \n"
#text += "a=100;\n"
#text = "fOr (i=1; i<a;i++) b = b+10*i; \n"
text = "multiplicacionescalar([1,2,3],3);"
#text += "#Aqui se devuelve el resultado esperado\n"
#text += "res = b * 0.8;"
#text = "LALLALALAL\npepe\n999$"
#
#text = "(inicio) = \"Hola\";\n"
#text += "x = capitalizar(inicio);"
#text = "a = {campo1: 4, campo2: \"hola\"}"
#text = "a = 3; b = a+4"
#text = "inicio = \"Hola\";\ni =0;"
#text = "inicio = True;"

lexer = lex(module=lexer_rules)
lexer.input(text)

token = lexer.token()

while token is not None:
	print token
	token = lexer.token()
