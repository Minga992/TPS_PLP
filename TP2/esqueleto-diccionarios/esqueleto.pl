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

juntar_con([R],Elem,R):-not(append(Head,[Elem | RTail],R)).
juntar_con([Head | Tail],Elem,R):-append(Head,[Elem | RTail],R), juntar_con(Tail,Elem,RTail).

palabras(S,P):-juntar_con(P,espacio,S).

% palabras(S,[S]):-not(append(X,[espacio | Y],S)).
% palabras(S,[X|P]):-append(X,[espacio | Y],S), palabras(Y,P).
