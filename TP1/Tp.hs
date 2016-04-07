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
quitarListVacias :: [[a]] -> [[a]]
quitarListVacias = foldr (\x xs -> if null x then xs else (x:xs)) []
--dada una lista de listas, remueve todas aquellas listas que sean vacias.


split :: Eq a => a -> [a] -> [[a]]

--Verision explicita:
--split d [] = []
--split d xs = takeWhile (\= d) xs : (split d tail(dropWhile (\= d) xs))

--split d [] = [[]]
--split d (x:xs) = if d == x then []:split(xs)
--       				   	else (x:head(split(xs))):tail(split(xs))

--Version final

split d ys = quitarListVacias (foldr (\x (xs:xss) -> if x == d then []:xs:xss else (x:xs):xss) [[]] ys)
-- si me encuentro con un delimitador, es una palabra aparte.  Si no, la letra es parte de la misma palabra.
-- quitarListVacias es un parche autorizado por pablo =P
-- explicitamos ys porque si no no tipa


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

-- Auxiliar
maxFstPar :: Num a => [(a,b)] -> (a,b)
maxFstPar (x:xs) = foldr (\y mfp-> if null xs then y else cond) x xs
						where cond = if (fst y) > (fst mfp) then y else mfp
-- Dada una lista de pares, devuelve el par con mayor valor en la primer componente

-- Auxiliar
kMin :: Num a => [(a,b)] -> [(a,b)] -> [(a,b)]
kMin xs ys = foldr (\z zs -> if (fst z) < fst (maxFstPar zs) then ns else zs) xs ys
				where ns = (takeWhile ((\=) (maxFstPar zs)) zs) ++ [z] ++ (tail (dropWhile (\=) (maxFstPar zs)) zs)
-- Dada dos listas de pares, que pretenden ser un prefijo y su correspondiente sufijo que completan una lista original, devuelve los k
-- elementos de la lista entera cuya primer componente es menor al resto. k esta determinado por el tamaño de la primer lista.

devolverEtiqueta :: [Etiqueta] -> Etiqueta
devolverEtiqueta xs = snd (maxFstPar (cuentas xs))
-- Dada unalista ded etiquetas, devuelve aquella etiqueta que aparezca una mayor cantidad de veces.

knn :: Int -> Datos -> [Etiqueta] -> Medida -> Modelo
knn k ds ls m = \xs -> devolverEtiqueta [snd p | p <- (kMin (take k ns) (drop k ns))]
						where ns = zip (map (m xs) ds) ls
-- Que alguien explique estoXD


accuracy :: [Etiqueta] -> [Etiqueta] -> Float
accuracy xs ys = (fromIntegral (sum (zipWith (\x y -> if x == y then 1 else 0) xs ys))) / (genericLength xs)

-- hay que ponerle algo a sum para que tipe con la division rara


-- Auxiliar
-- tomoParticionPe :: Int -> Int -> [a] -> [a]
-- tomoParticionPe n p xs = take (lxs * p) (drop (lxs * p) xs)
						-- where lxs = (genericLength xs)/n
-- Dada una lista de elementos, y dos enteros, uno que indica la cantidad de particiones de la lista en partes iguales,
-- y otro una particion en particular, devuelve los elementos que pertenecen a la particion particular

-- Auxiliar
-- noTomoParticionPe :: Int -> Int -> [a] -> [a]
-- noTomoParticionPe n p xs = (take (lxs * p) xs) ++ (drop (lxs * p) xs)
						  -- where lxs = (genericLength xs)/n

-- Dada una lista de elementos, y dos enteros, uno que indica la cantidad de particiones de la lista en partes iguales,
-- y otro una particion en particular, devuelve los elementos que no pertenecen a la particion particular
						  
-- Auxiliar -- sublista i f xs devuelve la sublista de xs entre los indices i y f inclusive
sublista :: Int -> Int -> [a] -> [a]
sublista i f = if i <= f then (take (f-i+1)).(drop i) else []

-- Auxiliar -- renombre de sublista para que se entienda mejor desp -- ver si poner como where
pTest :: Int -> Int -> [a] -> [a]
pTest = sublista

-- Auxiliar -- i y f son los indices del cacho para test, esto devuelve todo lo demas
pTrain :: Int -> Int -> [a] -> [a]
pTrain i f xs = (sublista 0 (i-1) xs) ++ (sublista (f+1) ((length xs)-1))

-- Auxiliar -- se encarga de dejarme la lista linda segun la cantidad de particiones que me piden
sacarSobr :: [a] -> Int -> [a]
sacarSobr xs n = take (((length xs)/n)*n) xs

separarDatos :: Datos -> [Etiqueta] -> Int -> Int -> (Datos, Datos, [Etiqueta], [Etiqueta])
separarDatos xs ys n p = (pTrain i f (sacarSobr xs n), pTest i f (sacarSobr xs n), pTrain i f (sacarSobr ys n), pTest i f (sacarSobr ys n))
						where i = ((length xs)/n)*(p-1)
							  f = (((length xs)/n)*p)-1
						
						-- if ((length xs) % n) == 0 
						-- then ((noTomoParticionPe n p xs),(tomoParticionPe n p xs),(noTomoParticionPe n p ys),(tomoParticionPe n p ys)) 
						-- else ((noTomoParticionPe n p (take lxsn xs)), (tomoParticionPe n p (take lxsn xs)),
						 	--  (noTomoParticionPe n p (take lxsn ys)), (tomoParticionPe n p (take lxsn ys)))
						-- where lxsn = ((genericLength xs)/n)*n

nFoldCrossValidation :: Int -> Datos -> [Etiqueta] -> Float
nFoldCrossValidation = undefined
