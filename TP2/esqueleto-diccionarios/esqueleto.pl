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

diccionario_lista(S):-diccionario(X), string_codes(X,S).

juntar_con([R],Elem,R):-not(append(_,[Elem | _],R)).
juntar_con([Head | Tail],Elem,R):-append(Head,[Elem | RTail],R), juntar_con(Tail,Elem,RTail).

palabras(S,P):-juntar_con(P,espacio,S).


asignar_var(A, MI, MI) :- member((A,_), MI).
asignar_var(A,MI,[(A,_) | MI]):-not(member((A,_),MI)).


atomos_a_variables([[Atom]], [[Var]], [(Atom,Var)]).
atomos_a_variables([[Atom] | AtomSS], [[Var] | VarSS], MF):-atomos_a_variables(AtomSS,VarSS,MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).
atomos_a_variables([[Atom | AtomS] | AtomSS], [[Var | VarS] | VarSS], MF):-atomos_a_variables([AtomS | AtomSS],[VarS | VarSS],MI), asignar_var(Atom,MI,MF), member((Atom,Var),MF).

palabras_con_variables(P, V):-atomos_a_variables(P,V,_).

%esto es una idea muy basica y pete, resaltado pete en este compilador, de quitar, esta mal, hay que pelearse con el hecho de no tener cosas instanseadas.
%quitar(Elem, [], []).
%quitar(Elem, [Elem|TaiL], HSE|TaiLSE) :- quitar(Elem, TaiL, [HSE| TaiLSE]).
%quitar(Elem, [Head|TaiL], HSE|TaiLSE) :- quitar(Elem, TaiL, TaiLSE), Elem \= Head, Elem \= HSE.

quitar(_,[],[]).
quitar(Elem,[Head|Tail],R) :- Elem == Head, quitar(Elem,Tail,R).
quitar(Elem,[Head|Tail],R) :- Elem \== Head, quitar(Elem,Tail,T), append([Head],T,R).


cant_distintos(L,Cant) :- list_to_set(L,S), length(S,Cant).

peleate_vos([],[]).
peleate_vos([S|TK],[S|TM]):- diccionario_lista(S), peleate_vos(TK,TM).

descifrar(S,B):- cant_distintos(S,Cant), palabras(S,H), palabras_con_variables(H,K), peleate_vos(K,M),juntar_con(M, 32, J), cant_distintos(J, Cant), string_codes(B, J).

espacios_everywhere([],[]).
espacios_everywhere([S],[S]).
espacios_everywhere([H,M|S], [H,espacio,M|P]):- espacios_everywhere([M|S],[M|P]). 
espacios_everywhere([H,M|S], [H,M|P]):- espacios_everywhere([M|S],[M|P]). 

descifrar_sin_espacios(S,M):- espacios_everywhere(S,P), descifrar(P,M).



%les presento codigo en pseudoprolog, con sexo oculto;)
%desvio_standard(Msje, Desvio):- string_codes(Msje, CodesMsje), juntar_con(CodesPalab, 32, CodesMsje), map(CodesPalab, length, LenghtsPalab),
%				sum_list(LenghtsPalab, TodasLasLetras), length(LenghtsPalab, CantPalab), 
%				MediaLongPalab is (TodasLasLetras / CantPalab), map(LenghtsPalab, - MediaLongPalab, FaltaElCuadrado),
%				map(FaltaElCuadrado, ^2, AhoraLaSumatoria), sum_list(AhoraLaSumatoria, DividimePorN),
%				Desvio is sqrt(DividimePorN / CantPalab).

longitudes_palabras(Msje,Longs) :- string_codes(Msje, CodesMsje), juntar_con(CodesPalab, 32, CodesMsje), longitudes(CodesPalab, Longs).

longitudes([],[]).
longitudes([X|XS],[L|LS]) :- length(X,L), longitudes(XS,LS).

restar_a_todos(_,[],[]).
restar_a_todos(M,[X|XS],[R|RS]) :- R is X-M, restar_media(M,XS,RS).

al_cuadrado([],[]).
al_cuadrado([X|XS],[C|CS]) :- C is X^2, al_cuadrado(XS,CS).

desvio_standard(Msje, Desvio):- longitudes_palabras(Msje,Longs), sum_list(Longs, SumaLongs), length(Longs, CantPalab), 
				Media is SumaLongs/CantPalab, restar_a_todos(Media,SumaLongs,FaltaElCuadrado),
				al_cuadrado(FaltaElCuadrado,AhoraLaSum),
				sum_list(AhoraLaSum,DividimePorN), Desvio is sqrt(DividimePorN/CantPalab).


el_mas_parejo(MSE, S):- desvio_standard(MSE, DesvStanMSE), not(descifrar_sin_espacios(S, MsjeDeComparacion), 
			desvio_standard(MsjeDeComparacion, DesvStanMDC), DesvStanMSE > DesvStanMDC). 

%setof(X,(descifrar_sin_espacios(S, MsjeDeComparacion), desvio_standard(MsjeDeComparacion, DesvStanMDC), mayor(DesvStanMSE, DesvStanMDC), X=MsjeDeComparacion), L), L = []. 

mensajes_mas_parejos(S,MsjeSinEspacios):- descifrar_sin_espacios(S, MsjeSinEspacios), el_mas_parejo(MsjeSinEspacios, S).


