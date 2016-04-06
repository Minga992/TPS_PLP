module Tp where

import Data.List

type Texto = String
type Feature = Float
type Instancia = [Feature]
type Extractor = (Texto -> Feature)

type Datos = [Instancia]
type Etiqueta = String
type Modelo = (Instancia -> Etiqueta)
type Medida = (Instancia -> Instancia -> Float)

tryClassifier :: [Texto] -> [Etiqueta] -> Float
tryClassifier x y = let xs = extraerFeatures ([longitudPromedioPalabras, repeticionesPromedio] ++ frecuenciaTokens) x in
    nFoldCrossValidation 5 xs y

mean :: [Float] -> Float
mean xs = realToFrac (sum xs) / genericLength xs

--Auxiliar
quitarListVacias :: Eq a => [[a]] -> [[a]]
quitarListVacias xs = foldr (\x xs -> if x==[] then xs else x:xs) []
--dada una lista de listas, remueve todas aquellas listas que sean vacias.


split :: Eq a => a -> [a] -> [[a]]

--Verision explicita:
--split d [] = []
--split d xs = takeWhile (\= d) xs : (split d tail(dropWhile (\= d) xs))

--split d [] = [[]]
--split d (x:xs) = if d == x then []:split(xs)
--       				   	else (x:head(split(xs))):tail(split(xs))

--Version final

split d = quitarListVacias (foldr (\x (xs:xss) -> if x == d then []:xs:xss else (x:xs):xss) [[]])
-- si me encuentro con un delimitador, es una palabra aparte.  Si no, la letra es parte de la misma palabra.


longitudPromedioPalabras :: Extractor
longitudPromedioPalabras xs = mean (map genericLength (split ' ' xs))
-- Sin los parentesis se ve horrible, pero la idea es, hago el split sacando los espacios del medio, eso me da una lista de listas,
-- le aplico map con genericLength, que dada una lista te devuelve su longitud en algun formato(supongo que es adaptable o algo asi,
-- o sino no entendi) y a eso le aplico mean que es una suerte de promedio.

--Auxiliar
cantAp :: Eq a => a -> [a] -> Int
cantAp d = foldr (\x acum -> (if x==d then 1 else 0) + acum ) 0
-- Ve la cantidad de apariciones de un elemento en una lista

--Auxiliar
noRep :: Eq a => [a] -> [a]
noRep = foldr (\x xs -> if elem x xs then xs else x:xs) []
--Devuelve una lista sin elementos repetidos.


cuentas :: Eq a => [a] -> [(Int, a)]

--Version explicita:
--cuentas [] 	 = []
--cuentas (x:xs) = (genericLength filter (= x) x:xs) : cuentas filter (\= x) x:xs

--se podria haber hecho con head, pero me parecio mas claro asi

--Version final:

cuentas xs = [(cantAp a xs, a) | a <- (noRep xs)]

repeticionesPromedio :: Extractor
repeticionesPromedio xs = mean (map (\xt -> fromIntegral (fst xt)) (cuentas (split ' ' xs)))
-- sencillo, hago split para separar en palabras,  hago cuentas para saber cuanto se repite cada palabra, aplico map y convierto
-- lo que me dio cuentas en solo numeros con formato Num hasta donde entendi, y de ahi pinto mean.

tokens :: [Char]
tokens = "_,)(*;-=>/.{}\"&:+#[]<|%!\'@?~^$` abcdefghijklmnopqrstuvwxyz0123456789"

frecuenciaTokens :: [Extractor]
frecuenciaTokens = [ \xs -> realToFrac (cantAp a xs) / genericLength xs | a <-tokens]
-- ACLARACION, use real to frac porque lo usaron ellos, se que tengo que aplicar algo, porque cantAp es int, pero no estoy seguro que
-- me armo una lista por comprension que tenga funciones que dado un xs toman su correspondiente token, y ven la frecuencia relativa.
-- si, no hay mucho que explicar aca(ALE)

--Auxiliar
-- normalizar :: Eq a =>  a -> Extractor -> Extractor
-- normalizar maxabs f = \xs -> f xs / maxabs
--dada una funcion, y un numero que va a ser el representante del 1.0 o del -1,0, normaliza al extractor

normalizarExtractor :: [Texto] -> Extractor -> Extractor
-- normalizarExtractor [] f = f 																--devuelvo algo, no se que hacer aca
-- normalizarExtractor xs f = normalizar (max (abs maximum map f xs) abs minimum map f xs) f

--Otra version, mas compacta

normalizarExtractor [] f = f
normalizarExtractor xs f = (\y -> y/n).f
			where n = max (abs (maximum (map f xs))) (abs (minimum (map f xs)))

-- la idea aca fue, conseguir al mayor en valor absoluto, ese chabon va a representar el 1.0 o el -1.0, depende el signo, y su opueto
-- va a representar al otro.Una vez que tengo eso, para normalizar simplemente hago que el extractor divida su resultado por este numero
-- obteniendo asi la proporcion deseada (explicacion tipo Utilisima (atentos a la mayuscula,no es por ser nombre propio)), el signo
-- va a estar dado por el signo original de lo que devolvia el extractor. 

--Auxiliar
extractoresNormalizados :: [Texto] -> [Extractor] -> [Extractor]
extractoresNormalizados ts exs = [normalizarExtractor ts ex | ex <- exs]

-- Dada una lista de extractores, y un texto de comparacion, normaliza los extractores de acuerdo a los textos.

--Auxiliar
featuresDelText :: Texto -> [Extractor] -> Instancia
featuresDelText t = foldr (\f fs -> f t : fs) []

-- Dado un texto y una lista de extractores, saca los features de aplicarle al texto todos los extractores.

extraerFeatures :: [Extractor] -> [Texto] -> Datos
extraerFeatures exs ts = [featuresDelText t ns | t <- ts]
						 where ns = extractoresNormalizados ts exs

-- La idea es que dado un grupo de extractores y un grupo de textos primero normalizo todos los extractores, y luego le aplico a cada 
-- texto todos los extractores normalizados por medio de la funncion featuresDelText

distEuclideana :: Medida
distEuclideana xs ys = sqrt (sum (zipWith (*) (zipWith (-) xs ys) (zipWith (-) xs ys)))
-- los zipWith (-) hacen p-q, el zipwith * hace la multiplicacion de ellos, obteniendo el cuadrado, sum adivinen, y sqrt les
-- hace la raiz cuadrado 

-- Auxiliar
prodEsc :: Num a => [a] -> [a] -> a
prodEsc xs ys = sum (zipWith (*) xs ys)

distCoseno :: Medida
distCoseno xs ys = prodEsc xs ys / ((sqrt (prodEsc xs xs)) * (sqrt (prodEsc ys ys)))
-- el ProdEsc hace el producto escalar de dos vectores, el puntito a medialtura para los amigos, luego de eso, la respuesta es
-- basicamente return lo que pide el enunciado en idioma imperativo... hay unos parentesis que podrian estar de mas, los puse 
-- solo por las dudas.

knn :: Int -> Datos -> [Etiqueta] -> Medida -> Modelo
knn = undefined

accuracy :: [Etiqueta] -> [Etiqueta] -> Float
accuracy = undefined

separarDatos :: Datos -> [Etiqueta] -> Int -> Int -> (Datos, Datos, [Etiqueta], [Etiqueta])
separarDatos = undefined

nFoldCrossValidation :: Int -> Datos -> [Etiqueta] -> Float
nFoldCrossValidation = undefined
