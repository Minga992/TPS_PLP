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

split :: Eq a => a -> [a] -> [[a]]
split d ys = filter (null) (foldr (\x (xs:xss) -> if x == d then []:xs:xss else (x:xs):xss) [[]] ys)
-- si me encuentro con un delimitador, es una palabra aparte.  Si no, la letra es parte de la misma palabra.
-- filter null es un parche autorizado por Pablo =P, quita todas las listas vacias
-- explicitamos ys porque si no no tipa

longitudPromedioPalabras :: Extractor
longitudPromedioPalabras xs = mean (map genericLength (split ' ' xs))
-- hago el split sacando los espacios del medio, eso me da una lista de listas,
-- le aplico map con genericLength para tener una lista con las longitudes, y a eso le aplico mean.

--Auxiliar -- Ve la cantidad de apariciones de un elemento en una lista
cantAp :: Eq a => a -> [a] -> Int
cantAp d = foldr (\x acum -> (if x==d then 1 else 0) + acum ) 0

--Auxiliar -- Dada una lista, la devuelve sin elementos repetidos.
--noRep :: Eq a => [a] -> [a]
--noRep = foldr (\x xs -> if elem x xs then xs else x:xs) []
-- lo dejo porque nub deja la primer ocurrencia, y hay que ver como afecta

cuentas :: Eq a => [a] -> [(Int, a)]
cuentas xs = [(cantAp a xs, a) | a <- (nub xs)] -- aca puse nub en vez de noRep
-- Devuelve los pares en un orden diferente al del ejemplo del enunciado

repeticionesPromedio :: Extractor
repeticionesPromedio xs = mean (map (\xt -> fromIntegral (fst xt)) (cuentas (split ' ' xs)))
-- sencillo, hago split para separar en palabras,  hago cuentas para saber cuanto se repite cada palabra, aplico map y convierto
-- lo que me dio cuentas en solo numeros con formato Num, y de ahi pinto mean.

tokens :: [Char]
tokens = "_,)(*;-=>/.{}\"&:+#[]<|%!\'@?~^$` abcdefghijklmnopqrstuvwxyz0123456789"

frecuenciaTokens :: [Extractor]
frecuenciaTokens = [ \xs -> realToFrac (cantAp a xs) / genericLength xs | a <-tokens]

normalizarExtractor :: [Texto] -> Extractor -> Extractor
normalizarExtractor [] f = f
normalizarExtractor xs f = (\y -> realToFrac y/n).f
			where n = max (abs (maximum (map f xs))) (abs (minimum (map f xs)))
-- la idea aca fue, conseguir al mayor en valor absoluto, que va a representar el 1.0 o el -1.0, depende el signo, y su opueto
-- va a representar al otro. Una vez que tengo eso, para normalizar simplemente hago que el extractor divida su resultado por este numero
-- obteniendo asi la proporcion deseada, el signo va a estar dado por el signo original de lo que devolvia el extractor. 

--Auxiliar -- Dada una lista de extractores, y un texto de comparacion, normaliza los extractores de acuerdo a los textos.
extractoresNormalizados :: [Texto] -> [Extractor] -> [Extractor]
extractoresNormalizados ts exs = [normalizarExtractor ts ex | ex <- exs]

--Auxiliar -- Dado un texto y una lista de extractores, saca los features de aplicarle al texto todos los extractores.
--featuresDelText :: Texto -> [Extractor] -> Instancia
--featuresDelText t = foldr (\f fs -> f t : fs) []
--lo dejo solo por las dudas, hasta que testeemos

extraerFeatures :: [Extractor] -> [Texto] -> Datos
extraerFeatures exs ts = [map (\f -> f t) ns | t <- ts] --aca decia featuresDelText t ns
						 where ns = extractoresNormalizados ts exs
-- La idea es que dado un grupo de extractores y un grupo de textos primero normalizo todos los extractores, y luego le aplico a cada 
-- texto todos los extractores normalizados por medio de la funncion featuresDelText

distEuclideana :: Medida
distEuclideana xs ys = sqrt (sum (map (**2) (zipWith (-) xs ys))) --esto fue modificado, le meti ese map

-- Auxiliar -- Producto escalar
prodEsc :: Num a => [a] -> [a] -> a
prodEsc xs ys = sum (zipWith (*) xs ys)

distCoseno :: Medida
distCoseno xs ys = prodEsc xs ys / ((sqrt (prodEsc xs xs)) * (sqrt (prodEsc ys ys)))

-- Auxiliar -- Dada una lista de pares, devuelve el par con mayor valor en la primer componente
maxFstPar :: Ord a => [(a,b)] -> (a,b)
maxFstPar (x:xs) = foldr (\y mfp-> if null xs then y else cond y mfp) x xs
						where cond = (\y mfp -> if (fst y) > (fst mfp) then y else mfp)

-- Auxiliar -- Dada dos listas de pares, que pretenden ser prefijo-sufijo (si las concateno tengo la lista completa),
			-- devuelve los k elementos de la lista entera cuya primer componente es menor al resto. 
			-- k esta determinado por el tamaño de la primer lista.
			-- La idea es, a cada paso, comparar el max de la primer lista con el siguiente elemento de la segunda.
			-- En caso de que el max sea mayor al otro, lo intercambio.  A la larga me quedan los k minimos en la primer lista.
kMin :: (Ord a, Eq b) => [(a,b)] -> [(a,b)] -> [(a,b)]
kMin xs = foldr (\z zs -> if (fst z) < fst (maxFstPar zs) then ns z zs else zs) xs
				where ns = (\z zs -> (takeWhile ((/=) (maxFstPar zs)) zs) ++ [z] ++ (tail (dropWhile ((/=) (maxFstPar zs)) zs)))

devolverEtiqueta :: [Etiqueta] -> Etiqueta
devolverEtiqueta xs = snd (maxFstPar (cuentas xs))
-- Dada una lista de etiquetas, devuelve aquella etiqueta que aparezca una mayor cantidad de veces.

knn :: Int -> Datos -> [Etiqueta] -> Medida -> Modelo
knn k ds ls m = (\xs -> devolverEtiqueta [snd p | p <- (kMin (take k (ns xs)) (drop k (ns xs)))])
						where ns = (\xs -> zip (map (m xs) ds) ls)
-- mapeo la medida entre la lista que me dan y la que tengo (datos) obteniendo una lista de numeritos,
-- zipeo esa lista de numeritos con su correspondiente etiqueta, separo la lista resultante en dos listas:
-- los k primeros y el resto, con eso busco los k minimos respecto de la distancia (fst del par) y me fijo
-- que etiqueta se repite mas veces

accuracy :: [Etiqueta] -> [Etiqueta] -> Float
accuracy xs ys = (sum (zipWith (\x y -> if x == y then 1.0 else 0.0) xs ys)) / (genericLength xs)

-- Auxiliar -- sublista i f xs devuelve la sublista de xs entre los indices i y f inclusive
sublista :: Int -> Int -> [a] -> [a]
sublista i f = if i <= f then (take (f-i+1)).(drop i) else (const [])

-- Auxiliar -- i y f son los indices del cacho para test, esto devuelve todo lo demas
pTrain :: Int -> Int -> [a] -> [a]
pTrain i f xs = (sublista 0 (i-1) xs) ++ (sublista (f+1) ((length xs)-1) xs)

-- Auxiliar -- se encarga de dejarme la lista linda segun la cantidad de particiones que me piden
sacarSobr :: [a] -> Int -> [a]
sacarSobr xs n = take (((length xs) `div` n)*n) xs

separarDatos :: Datos -> [Etiqueta] -> Int -> Int -> (Datos, Datos, [Etiqueta], [Etiqueta])
separarDatos xs ys n p = let 
							i = ((length xs) `div` n)*(p-1)
							f = (((length xs) `div` n)*p)-1
							pTest = sublista
						in (pTrain i f (sacarSobr xs n), pTest i f (sacarSobr xs n), pTrain i f (sacarSobr ys n), pTest i f (sacarSobr ys n))
						
-- Auxiliar -- Dada una cuatrupla devuelve su primer componente => datos de entrenamiento
dTrain :: (a,b,c,d) -> a
dTrain (w,x,y,z) = w

-- Auxiliar -- Dada una cuatrupla devuelve su segunda componente => datos de validacion
dVal :: (a,b,c,d) -> b
dVal (w,x,y,z) = x

-- Auxiliar -- Dada una cuatrupla devuelve su tercer componente => etiquetas de entrenamiento
lTrain :: (a,b,c,d) -> c
lTrain (w,x,y,z) = y

-- Auxiliar -- Dada una cuatrupla devuelve su cuarta componente => etiquetas de validacion
lVal :: (a,b,c,d) -> d
lVal (w,x,y,z) = z

-- Auxiliar -- Dada una lista de cuatruplas con datos y etiquetas separados por training y validacion, 
			-- devuelvo las etiquetas que devuelve nuestro modelo aplicado a cada instancia de prueba. 
			-- Ver que uso map, porque a mi modelo entrenado le paso muchas instancias, no una sola.
			-- Hardcodeamos 15 y distEuclideana porque lo dice el enunciado.
obtenerEtiquetas :: [(Datos, Datos, [Etiqueta], [Etiqueta])] -> [[Etiqueta]]
obtenerEtiquetas = foldr (\x xs -> (map (knn 15 (dTrain x) (lTrain x) distEuclideana) (dVal x)) : xs ) []

nFoldCrossValidation :: Int -> Datos -> [Etiqueta] -> Float
nFoldCrossValidation n ds es = mean (zipWith accuracy (obtenerEtiquetas ns) etireales)
								where 
									ns = [separarDatos ds es n i |i <- [1..n]]
									etireales = map lVal ns
-- la idea aca es primero obtener una lista con los datos ordenados segun los de entrenamiento y los de prueba para cada particion,
-- eso sucede en ns. Luego, con obtener etiquetas entrene mis modelos y veo que etiqueta me tiran a cada prueba, luego mido el
-- porcentaje de aciertos respecto a las verdaderas etiquetas, y al final calculo el promedio.
