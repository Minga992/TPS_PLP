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

% juntar_con(+Lista1,?Elem,?Lista2)
% Da True si, siendo Lista1 una lista de listas, Lista2 es la concatenación de las listas de Lista1, con el elemento Elem entre los elementos de dos listas distintas
% Lista1 debe estar instanciada, de lo contrario juntar_con se cuelga.
juntar_con([],_,[]).
juntar_con([R],_,R).
juntar_con([HeadL,NexToHeadL | TaiLL],Elem, LseparConElem):- append(HeadL,[Elem],PrimeraParte), 
							     juntar_con([NexToHeadL|TaiLL],Elem,SeguiSeparando),
							     append(PrimeraParte,SeguiSeparando,LseparConElem).

% palabras(+S,?P)
% da true si S concatena las sublistas de P separando por 'espacio'.
% S debe instanciarse ya que si sólo se instancia P da resultados inesperados.
palabras(R,[R]):-not(append(_,[espacio | _],R)).
palabras(R,[Head | Tail]):-append(Head,[espacio | RTail],R), not(member(espacio,Head)), palabras(RTail,Tail).

%separar_por_palabras([R],Elem,R):-not(append(_,[Elem | _],R)).
%separar_por_palabras([Head | Tail],Elem,R):-append(Head,[Elem | RTail],R), not(member(Elem,Head)), juntar_con(Tail,Elem,RTail).

% palabras(?S,?P)
% al menos uno de los dos parámetros debe instanciarse (ver juntar_con/3)
%palabras(S,P):-separar_por_palabras(P,espacio,S).



% asignar_var(?A,?MI,?MF)
% si se instancian las 3 variables, da true cuando MF es el resultado de agregar (A,_variable) a MI en caso de que no estuviera, o MF = MI si ya estaba.
% si se instancian las variables de a 2, asignar_var/3 es reversible.
% si se instancia sólo una, tiene que ser MF, en otro caso da infinitos resultados con las posibilidades completadas con variables.
% si no se instancia ninguna variable, el comportamiento no es el esperado.
asignar_var(A, MI, MI) :- member((A,_), MI).
asignar_var(A,MI,[(A,_) | MI]):-not(member((A,_),MI)).

% atomos_a_variables(+Lista1,?Lista2,?Lista3) 
% da true si Lista3 contiene los pares formados por los elementos de Lista1 y Lista2, en el orden en el que vienen, y para cada primer coordenada existe sólo 1 segunda coordenada (ejemplo: no pueden estar (3,4) y (3,5) a la vez).  No hay repetidos en Lista3.
% Lista1 debe estar instanciada porque de lo contrario puede colgarse, fallar o tener un comportamiento no esperado.
atomos_a_variables([[Atom]], [[Var]], [(Atom,Var)]).
atomos_a_variables([[Atom] | AtomSS], [[Var] | VarSS], MF):-atomos_a_variables(AtomSS,VarSS,MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).
atomos_a_variables([[Atom | AtomS] | AtomSS], [[Var | VarS] | VarSS], MF):-atomos_a_variables([AtomS | AtomSS],[VarS | VarSS],MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).

% palabras_con_variables(+P,?V)
% Ver atomos_a_variables/3.
palabras_con_variables([[]],[[]]).
palabras_con_variables(P, V):-atomos_a_variables(P,V,_).

% quitar(?Elem,+Lista1,?Lista2)
% da true si Lista2 es Lista1 quitando las apariciones de Elem.
% Lista1 debe estar instanciada, ya que de lo contrario se busca unificar Lista1 y Lista2, lo cual no es la idea del predicado.
% el predicado (==)/2 chequea por equivalencia, no por unificación, lo cual permite comparar variables no instanciadas y distinguirlas, tanto de otras variables como de elementos instanciados.
quitar(_,[],[]).
quitar(Elem,[Head|Tail],R) :- Elem == Head, quitar(Elem,Tail,R).
quitar(Elem,[Head|Tail],R) :- Elem \== Head, quitar(Elem,Tail,T), append([Head],T,R).

% cant_distintos(+L,?C)
% da true si C es la cantidad de elementos distintos en L.
% L debe instanciarse para que funcione list_to_set/2.
cant_distintos(L,Cant) :- list_to_set(L,S), length(S,Cant).

% armar_mensaje(+Lista)
% unifica las variables de Lista con palabras del diccionario (pasadas a ascii).
% la variable debe instanciarse, ya que de lo contrario posee un comportamiento no esperado.
armar_mensaje([]).
armar_mensaje([S|TK]):- diccionario_lista(S), armar_mensaje(TK).

% descifrar(+S,?B)
% B es la decodificación de la frase codificada en S.
% S debe estar instanciada por el funcionamiento de cant_distintos/2.
descifrar(S,B):- cant_distintos(S,Cant), palabras(S,H), palabras_con_variables(H,M), armar_mensaje(M),juntar_con(M, 32, J), cant_distintos(J, Cant), string_codes(B, J).

% espacios_everywhere(?Lista1,?Lista2)
% da true si Lista2 contiene los mismos elementos que Lista1 en el mismo orden, eventualmente con espacios intercalados.
% si sólo se instancia Lista1, Lista2 es instanciada con todas las posibles combinaciones de espacios entre los elementos de Lista1.
% si sólo se instancia Lista2, Lista1 es instanciada con todas las posibles formas de quitar algún espacio de los elementos de Lista2.
% no debe no instanciarse ninguna, de lo contrario el comportamiento no es el esperado.
espacios_everywhere([],[]).
espacios_everywhere([S],[S]).
espacios_everywhere([H,M|S], [H,espacio,M|P]):- espacios_everywhere([M|S],[M|P]). 
espacios_everywhere([H,M|S], [H,M|P]):- espacios_everywhere([M|S],[M|P]). 

% descifrar_sin_espacios(+S,?M)
% S debe estar instanciada por el comportamiento de espacios_everywhere/2.
descifrar_sin_espacios(S,M):- espacios_everywhere(S,P), descifrar(P,M).

% longitudes_palabras(+Msje,?Lista)
% da true si Lista contiene las longitudes de las palabras del string Msje.
% Msje debe estar instanciada porque string_codes/2 no funciona con dos variables no instanciadas.
longitudes_palabras(Msje,Longs) :- string_codes(Msje, CodesMsje), juntar_con(CodesPalab, 32, CodesMsje), longitudes(CodesPalab, Longs).

% longitudes(?Lista1,?Lista2)
% da true si Lista2 mapea las longitudes de las listas de Lista1.
% no debe no instanciarse ninguna, de lo contrario el comportamiento no es el esperado.
longitudes([],[]).
longitudes([X|XS],[L|LS]) :- length(X,L), longitudes(XS,LS).

% restar_a_todos(+M,+Lista1,-Lista2)
% instancia Lista2 en una lista con los elementos de Lista1 restándole a cada uno el valor M.
% M y Lista1 deben instanciarse por el funcionamiento de 'is' en la segunda declaración (lo de la derecha del 'is' no puede no estar instanciado).
restar_a_todos(_,[],[]).
restar_a_todos(M,[X|XS],[R|RS]) :- R is X-M, restar_a_todos(M,XS,RS).

% al_cuadrado(+Lista1,-Lista2)
% instancia Lista2 en una lista con los elementos de Lista1 al cuadrado.
% Lista1 debe instanciarse por el funcionamiento de 'is' en la segunda declaración (lo de la derecha del 'is' no puede no estar instanciado).
al_cuadrado([],[]).
al_cuadrado([X|XS],[C|CS]) :- C is X^2, al_cuadrado(XS,CS).

% desvio_standard(+Msje,-Desvio)
% instancia Desvio en el desvio standard de las longitudes de las palabras del string Msje.
% Msje debe estar instanciado por el funcionamiento de longitudes_palabras/2.
desvio_standard(Msje, Desvio):- longitudes_palabras(Msje,Longs), sum_list(Longs, SumaLongs), length(Longs, CantPalab), 
				Media is SumaLongs/CantPalab, restar_a_todos(Media,Longs,FaltaElCuadrado),
				al_cuadrado(FaltaElCuadrado,AhoraLaSum),
				sum_list(AhoraLaSum,DividimePorN), Desvio is sqrt(DividimePorN/CantPalab).

% el_mas_parejo(+MSE,+S)
% da true si el string MSE tiene el menor desvío standard de las longitudes de las palabras que cualquier otro mensaje descifrado a partir de S.
% las variables deben instanciarse por el funcionamiento de desvio_standard/2 y descifrar_sin_espacios/2.
el_mas_parejo(MSE, S):- desvio_standard(MSE, DesvStanMSE), not((descifrar_sin_espacios(S, MsjeDeComparacion), 
			desvio_standard(MsjeDeComparacion, DesvStanMDC), DesvStanMSE > DesvStanMDC)). 

% mensajes_mas_parejos(+S,?M)
% S debe instanciarse por el funcionamiento de descifrar_sin_espacios/2.
mensajes_mas_parejos(S,MsjeSinEspacios):- descifrar_sin_espacios(S, MsjeSinEspacios), el_mas_parejo(MsjeSinEspacios, S).

%ej1
%Con dicc0:

% diccionario_lista(S).
% S = [101, 108] ; %% "el"
% S = [108, 97] ; %% "la"
% S = [99, 97, 115, 97] ; %% "casa"
% S = [99, 111, 115, 97]. %% "cosa"

% diccionario_lista([101, 108]). %% "el"
% true ;
% false.

% diccionario_lista([99, 97, 115, 111]). %% "caso"
% false.


%ej2
% juntar_con([[d],[c,b],[a,c,a]],espacio,R).
% R = [d, espacio, c, b, espacio, a, c, a] ;
% false.

% juntar_con([[d,espacio],[c,b],[espacio,a,c,a]],espacio,R).
% R = [d, espacio, espacio, c, b, espacio, espacio, a, c, a] ;
% false.

% juntar_con([[d,espacio],[espacio,c,b,espacio],[espacio,a,c,a]],espacio,R).
% R = [d, espacio, espacio, espacio, c, b, espacio, espacio, espacio, a, c, a] ;
% false.


%ej3
% palabras( [d, espacio, c, b, espacio, a, c, a], P).
% P = [[d], [c, b], [a, c, a]] ;
% false.

% palabras( [d, c, b, a, c, a], P).
% P = [[d, c, b, a, c, a]] ;
% false.


%ej4
% asignar_var(cuadrado, [], M).
% M = [ (cuadrado, _G23020)].

% asignar_var(cuadrado, [(triangulo,_G23021)], M).
% M = [ (cuadrado, _G23161), (triangulo, _G23021)].

% asignar_var(triangulo,  [(cuadrado, _G23161), (triangulo, _G23021)], M).
% M = [ (cuadrado, _G23161), (triangulo, _G23021)] ;
% false.

%ej5
% palabras_con_variables([[rombo,triangulo],[rombo,cuadrado],[circulo,triangulo,cuadrado]],V).
% V = [[_G88880, _G88889], [_G88880, _G88904], [_G88910, _G88889, _G88904]] ;
% false.

% palabras_con_variables([[rombo,rombo],[rombo,rombo],[rombo,rombo,rombo]],V).
% V = [[_G88784, _G88784], [_G88784, _G88784], [_G88784, _G88784, _G88784]] ;
% false.

% palabras_con_variables([[rombo,triangulo],[estrella,cuadrado],[circulo,perro,gato]],V).
% V = [[_G88850, _G88859], [_G88865, _G88874], [_G88880, _G88889, _G88898]] ;
% false.


%ej6

% quitar(z,[A,B,A,z],L).
% L = [A, B, A] ;
% false.

% quitar(A,[A,B,A,z],L).
% L = [B, z] ;
% false.

% quitar(C,[A,B,A,z],L).
% L = [A, B, A, z].

% quitar(z,[z,A,z,B,A,z,zz,Z],L).
% L = [A, B, A, zz, Z] ;
% false.

% quitar(a,[A,B,A,z],L).
% L = [A, B, A, z].


%ej7

% cant_distintos([A,B,A], N).
% N = 2.

% cant_distintos([A,B,skd,A,z,sjf], N).
% N = 5.

% cant_distintos([A,B,skd,A,z,sjf,z], N).
% N = 5.

% cant_distintos([a,b,c,b], N).
% N = 3.


%ej8
%Con 10000_formas:

% descifrar([rombo, cuadrado, espacio, perro, cuadrado, gato, cuadrado, espacio, estrella, arbol, triangulo, espacio, triangulo, circulo, gato, circulo], M).
% M = "de jefe por rafa" ;
% M = "de jefe sur rafa" ;
% M = "de jefe sor rafa" ;
% M = "de jefe mir rafa" ;
% M = "de pese ugt tasa" ;
% M = "de pese com masa" ;
% M = "de pese tom masa" ;
% M = "de tele nos sala" .

% descifrar([rombo, cuadrado, perro, cuadrado, gato, cuadrado, estrella, arbol], M).
% M = "dirigió" ;
% M = "dolorosa" ;
% false.


%ej9
%Con dicc1:

% descifrar_sin_espacios([rombo, cuadrado, perro, cuadrado, sol, luna, triangulo, estrella, arbol, gato], M).
% M = "casa de flor" ;
% M = "casa flor de" ;
% M = "casa miento" ;
% false.

%ej10




