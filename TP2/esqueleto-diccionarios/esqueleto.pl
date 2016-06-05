:- dynamic(diccionario/1).

% Dado un nombre de archivo que contiene todas las palabras que se quieren
% agregar al diccionario (una por linea), vacia diccionario/1 y agrega
% las definiciones nuevas

cargar(NombreDeArchivo) :-
  retractall(diccionario(_)),
  atom_codes(NombreDeArchivo, Arch),
  open(Arch, read, Str),
  read_file(Str,_),
  close(Str).

read_file(Stream,[]) :- at_end_of_stream(Stream).
read_file(Stream,[X|L]) :-
    not(at_end_of_stream(Stream)),
    read_line_to_codes(Stream,Codes),
    string_codes(X, Codes),
    assertz(diccionario(X)),
    read_file(Stream,L), !.


% listar mensajes secretos de ejemplo.
ej(1, [rombo, cuadrado, espacio, perro, cuadrado, sol, cuadrado]).
% solo debería ser "la cosa" porque cuadrado != triangulo
ej(2, [rombo, cuadrado, espacio, perro, triangulo, sol, cuadrado]).

ej(3, [rombo, cuadrado, perro, cuadrado, sol, luna, triangulo, estrella, arbol, gato]).

% diccionario_lista(?S)
% si no se instancia S, la va instanciando en las listas de ascii correspondientes a las palabras del diccionario actual.
% si se instancia S, da true si hay una palabra en el diccionario actual con esos ascii.
diccionario_lista(S):-diccionario(X), string_codes(X,S).

% juntar_con(?Lista1, ?Elem, ?Lista2)
% da true si Lista2 concatena las sublistas de Lista1 separando por Elem.
% si sólo se instancia Lista1 da false, fallando en 'not(member(Elem,Head))', ya que basta tomar Elem = Head.
% si sólo se instancia Elem, falla al no poder instanciar los parámetros de append/3.
% si sólo se instancia Lista2, arroja los resultados posibles para Lista1 y Elem.
juntar_con([R],Elem,R):-not(append(_,[Elem | _],R)).
juntar_con([Head | Tail],Elem,R):-append(Head,[Elem | RTail],R), not(member(Elem,Head)), juntar_con(Tail,Elem,RTail).

% palabras(?S,?P)
% al menos uno de los dos parámetros debe instanciarse (ver juntar_con/3)
palabras(S,P):-juntar_con(P,espacio,S).

% asignar_var(?A,?MI,?MF)
% funciona con cualquier cantidad de variables instanciadas (incluso 0) debido al funcionamiento de member/2.
asignar_var(A, MI, MI) :- member((A,_), MI).
asignar_var(A,MI,[(A,_) | MI]):-not(member((A,_),MI)).

% atomos_a_variables(Lista1,Lista2,Lista3) TERMINAR ESTE
% da true si Lista3 contiene los pares formados por los elementos de Lista1 y Lista2, en el orden en el que vienen, y para cada primer coordenada existe sólo 1 segunda coordenada (ejemplo: no pueden estar (3,4) y (3,5) a la vez).  No hay repetidos en Lista3.
atomos_a_variables([[Atom]], [[Var]], [(Atom,Var)]).
atomos_a_variables([[Atom] | AtomSS], [[Var] | VarSS], MF):-atomos_a_variables(AtomSS,VarSS,MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).
atomos_a_variables([[Atom | AtomS] | AtomSS], [[Var | VarS] | VarSS], MF):-atomos_a_variables([AtomS | AtomSS],[VarS | VarSS],MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).

% palabras_con_variables(P,V) TERMINAR ESTE
palabras_con_variables(P, V):-atomos_a_variables(P,V,_).

% quitar(?Elem,?Lista1,?Lista2)
% da true si Lista2 es Lista1 quitando las apariciones de Elem.
% si Elem no se instancia y las listas sí, da true si las listas son iguales y false en caso contrario, por la tercera declaración.
% si Lista1 no se instancia y Lista2 sí, unifica Lista2 con Lista1, y si se pide una nueva solución se cuelga en la tercera declaración.
% si Lista2 no se instancia y Lista1 sí, instancia Lista2 como Lista1 sin Elem.
% si no se instancian ni Elem ni Lista2, instancia Lista2 en Lista1.
% si sólo se instancia Elem, genera infinitas Lista1 = Lista2.
quitar(_,[],[]).
quitar(Elem,[Head|Tail],R) :- Elem == Head, quitar(Elem,Tail,R).
quitar(Elem,[Head|Tail],R) :- Elem \== Head, quitar(Elem,Tail,T), append([Head],T,R).

% cant_distintos(+L,?C)
% da true si C es la cantidad de elementos distintos en L.
% L debe instanciarse para que funcione list_to_set/2.
cant_distintos(L,Cant) :- list_to_set(L,S), length(S,Cant).

% CAMBIAME EL NOMBREEE
peleate_vos([],[]).
peleate_vos([S|TK],[S|TM]):- diccionario_lista(S), peleate_vos(TK,TM).

% descifrar(S,B)  TERMINAR ESTE
descifrar(S,B):- cant_distintos(S,Cant), palabras(S,H), palabras_con_variables(H,K), peleate_vos(K,M),juntar_con(M, 32, J), cant_distintos(J, Cant), string_codes(B, J).

% espacios_everywhere(?Lista1,?Lista2)
% da true si Lista2 contiene los mismos elementos que Lista1 en el mismo orden, eventualmente con espacios entre ellos.
% si sólo se instancia Lista1, Lista2 es instanciada con todas las posibles combinaciones de espacios entre los elementos de Lista1.
% si sólo se instancia Lista2, Lista1 es instanciada con todas las posibles formas de quitar algún espacio de los elementos de Lista2.
% puede no instanciarse ninguna de las dos, esto generará sucesivas Lista1 incrementando en uno la longitud cada vez, y una Lista2 para cada Lista1 con todos los posibles espacios incluidos.
espacios_everywhere([],[]).
espacios_everywhere([S],[S]).
espacios_everywhere([H,M|S], [H,espacio,M|P]):- espacios_everywhere([M|S],[M|P]). 
espacios_everywhere([H,M|S], [H,M|P]):- espacios_everywhere([M|S],[M|P]). 

% descifrar_sin_espacios(S,M)  TERMINAR ESTE
descifrar_sin_espacios(S,M):- espacios_everywhere(S,P), descifrar(P,M).

% longitudes_palabras(+Msje,?Lista)
% da true si Lista contiene las longitudes de las palabras del string Msje.
% Msje debe estar instanciada porque string_codes/2 no funciona con dos variables no instanciadas.
longitudes_palabras(Msje,Longs) :- string_codes(Msje, CodesMsje), juntar_con(CodesPalab, 32, CodesMsje), longitudes(CodesPalab, Longs).

% longitudes(?Lista1,?Lista2)
% da true si Lista2 mapea las longitudes de las listas de Lista1.
longitudes([],[]).
longitudes([X|XS],[L|LS]) :- length(X,L), longitudes(XS,LS).

% restar_a_todos(+M,+Lista1,?Lista2)
% da true si Lista2 contiene los elementos de Lista1 restándoles el valor M.
% M y Lista1 deben instanciarse por el funcionamiento de 'is' en la segunda declaración (lo de la derecha del 'is' no puede no estar instanciado).
restar_a_todos(_,[],[]).
restar_a_todos(M,[X|XS],[R|RS]) :- R is X-M, restar_a_todos(M,XS,RS).

% al_cuadrado(+Lista1,?Lista2)
% da true si Lista2 contiene los elementos de Lista1 al cuadrado.
% Lista1 debe instanciarse por el funcionamiento de 'is' en la segunda declaración (lo de la derecha del 'is' no puede no estar instanciado).
al_cuadrado([],[]).
al_cuadrado([X|XS],[C|CS]) :- C is X^2, al_cuadrado(XS,CS).

% desvio_standard(+Msje,?Desvio)
% da true si Desvio es el desvio standard de las longitudes de las palabras del string Msje.
% Msje debe estar instanciado por el funcionamiento de longitudes_palabras/2.
desvio_standard(Msje, Desvio):- longitudes_palabras(Msje,Longs), sum_list(Longs, SumaLongs), length(Longs, CantPalab), 
				Media is SumaLongs/CantPalab, restar_a_todos(Media,Longs,FaltaElCuadrado),
				al_cuadrado(FaltaElCuadrado,AhoraLaSum),
				sum_list(AhoraLaSum,DividimePorN), Desvio is sqrt(DividimePorN/CantPalab).

% el_mas_parejo(+MSE,S) TERMINAR ESTE
el_mas_parejo(MSE, S):- desvio_standard(MSE, DesvStanMSE), not((descifrar_sin_espacios(S, MsjeDeComparacion), 
			desvio_standard(MsjeDeComparacion, DesvStanMDC), DesvStanMSE > DesvStanMDC)). 

% mensajes_mas_parejos(S,M) TERMINAR ESTE
mensajes_mas_parejos(S,MsjeSinEspacios):- descifrar_sin_espacios(S, MsjeSinEspacios), el_mas_parejo(MsjeSinEspacios, S).


