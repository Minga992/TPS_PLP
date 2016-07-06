reserved = {
	'begin' : 'BEGIN',
	'end' : 'END',
	'while' : 'WHILE',
	'for' : 'FOR',
	'if' : 'IF',
	'else' : 'ELSE',
	'do' : 'DO',
	'res' : 'RES',
	'return' : 'RETURN',
	'AND' : 'AND',
	'OR' : 'OR',
	'NOT' : 'NOT',
	'print' : 'PRINT',
	'multiplicacionescalar' : 'MULTESC',
	'capitalizar' : 'CAP',
	'colineales' : 'COLIN',
	'length' : 'LENGTH'
}

tokens = [
	#tipos y variables
	'STR',
	'BOOL',
	'NUM',
	'VAR',
	#signos de puntuacion
	'PUNTO',
	'DOSPTOS',
	'COMA',
	'ADM',
	'PREG',
	'PTOCOMA',	
	#signos de a pares
	'LCORCH',
	'RCORCH',
	'LPAREN',
	'RPAREN',
	'LLLAVE',
	'RLLAVE',
	#signos aritmeticos
	'MAS',
	'MENOS',
	'IGUAL',
	'POR',
	'DIV',
	'POT',
	'MOD',
	'MAYOR',
	'MENOR',
	#comentarios
	'COMENT'
] + list(reserved.values())


#Reglas simples
t_PUNTO = r"\."
t_DOSPTOS = r"\:"
t_COMA = r"\,"
t_ADM = r"\!"
t_PREG = r"\?"
t_PTOCOMA = r";"
t_LCORCH = r"\["
t_RCORCH = r"\]"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LLLAVE = r"\{"
t_RLLAVE = r"\}"
t_MAS = r"\+"
t_MENOS = r"\-"
t_IGUAL = r"\="
t_POR = r"\*"
t_DIV = r"/"
t_POT = r"\^"
t_MOD = r"%"
t_MAYOR = r"\>"
t_MENOR = r"\<"


#Reglas Complejas
def t_STR(token):
	r"\"[^\"]*\""
	
	return token
	
	
def t_BOOL(token):
	r"([tT][rR][uU][eE] | [fF][aA][lL][sS][eE])"
	
	if (token.value).lower() == 'true':
		token.value = True
	elif (token.value).lower() == 'false':
		token.value = False
		
	return token


def t_NUM(token):
	r"[0-9]+"
	
	token.value = int(token.value)
	
	return token

	
def t_VAR(token):
	r"[a-zA-Z][a-zA-Z0-9_]*"
	
	token.type = reserved.get((token.value).lower(),'VAR')    # Check for reserved words
	
	if token.type in ['BEGIN','END','RETURN']:
		palabra_reservada(token)
	
	return token


def t_COMENT(token):
	r"\#.*"
	return token


#Se ignoran espacios y tabulados
t_ignore_WHITESPACES = r"[ \t]+"


def t_NEWLINE(token):
	r"\n+"
	token.lexer.lineno += len(token.value)


def t_error(token):
	message = "Token desconocido:"
	message += "\ntype:" + token.type
	message += "\nvalue:" + str(token.value)
	message += "\nline:" + str(token.lineno)
	message += "\nposition:" + str(token.lexpos)
	raise Exception(message)
	
	
def palabra_reservada(token):
	message = "Palabra reservada no utilizable:"
	message += "\ntype:" + token.type
	message += "\nvalue:" + str(token.value)
	message += "\nline:" + str(token.lineno)
	message += "\nposition:" + str(token.lexpos)
	raise Exception(message)
	
