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
split d ys = filter (not.null) (foldr (\x (xs:xss) -> if x == d then []:xs:xss else (x:xs):xss) [[]] ys)
-- si me encuentro con un delimitador, es una palabra aparte.  Si no, la letra es parte de la misma palabra.
-- filter (not.null) es un parche autorizado por Pablo =P, quita todas las listas vacias
-- explicitamos ys porque si no no tipa

longitudPromedioPalabras :: Extractor
longitudPromedioPalabras xs = mean (map genericLength (split ' ' xs))
-- hago el split sacando los espacios del medio, eso me da una lista de listas,
-- le aplico map con genericLength para tener una lista con las longitudes, y a eso le aplico mean.

--Auxiliar -- Ve la cantidad de apariciones de un elemento en una lista
cantAp :: Eq a => a -> [a] -> Int
cantAp d = foldr (\x acum -> (if x==d then 1 else 0) + acum ) 0

cuentas :: Eq a => [a] -> [(Int, a)]
cuentas xs = [(cantAp a xs, a) | a <- (nub xs)]

repeticionesPromedio :: Extractor
repeticionesPromedio xs = mean (map (\xt -> fromIntegral (fst xt)) (cuentas (split ' ' xs)))
-- se hace split para separar en palabras y cuentas para saber cuanto se repite cada palabra, aplicamos map 
-- y convertimos lo que dio cuentas en solo numeros con formato Num.  A eso se aplica mean.

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

extraerFeatures :: [Extractor] -> [Texto] -> Datos
extraerFeatures exs ts = [map (\f -> f t) extrNorm | t <- ts]
						 where extrNorm = extractoresNormalizados ts exs
-- La idea es que dado un grupo de extractores y un grupo de textos, primero normalizo todos los extractores, 
-- y luego le aplico a cada texto todos los extractores normalizados.

distEuclideana :: Medida
distEuclideana xs ys = sqrt (sum (map (**2) (zipWith (-) xs ys)))

-- Auxiliar -- Producto escalar
prodEsc :: Num a => [a] -> [a] -> a
prodEsc xs ys = sum (zipWith (*) xs ys)

distCoseno :: Medida
distCoseno xs ys = prodEsc xs ys / ((sqrt (prodEsc xs xs)) * (sqrt (prodEsc ys ys)))

knn :: Int -> Datos -> [Etiqueta] -> Medida -> Modelo
knn k ds ls m = (\ins -> modaEstadistica (etiquetasDeKVecinosMasCercanos (zip (distanciasATodasLasInstancias ins) ls)))
						where 
							distanciasATodasLasInstancias = (\ins -> map (m ins) ds)
							etiquetasDeKVecinosMasCercanos = (\dists -> [snd p | p <- (kVecinosMasCercanos dists)])
							modaEstadistica = (\xs ->  snd (last (sort (cuentas xs))))
							kVecinosMasCercanos = (\dists -> take k (sort dists))
-- Dada una instancia, se calcula la moda estadistica de las etiquetas de los k vecinos mas cercanos a esa instancia

accuracy :: [Etiqueta] -> [Etiqueta] -> Float
accuracy xs ys = (sum (zipWith (\x y -> if x == y then 1.0 else 0.0) xs ys)) / (genericLength xs)

-- Auxiliar -- sublista i f xs devuelve la sublista de xs entre los indices i y f inclusive
sublista :: Int -> Int -> [a] -> [a]
sublista i f = if i <= f then (take (f-i+1)).(drop i) else (const [])

-- Auxiliar -- sacarSublista i f xs devuelve la lista resultante de sacar de xs la sublista entre los indices i y f inclusive
sacarSublista :: Int -> Int -> [a] -> [a]
sacarSublista i f xs = (sublista 0 (i-1) xs) ++ (sublista (f+1) ((length xs)-1) xs)

-- Auxiliar -- se encarga de que la cantidad de elementos de xs sea divisible por n.
			-- si no era divisible, elimina los elementos sobrantes del final.
sacarSobr :: [a] -> Int -> [a]
sacarSobr xs n = take (((length xs) `div` n)*n) xs

separarDatos :: Datos -> [Etiqueta] -> Int -> Int -> (Datos, Datos, [Etiqueta], [Etiqueta])
separarDatos xs ys n p = (datosTrain, datosTest, etiqTrain, etiqTest)
							where
								datosTrain = sacarSublista initP finP (sacarSobr xs n)
								datosTest = sublista initP finP (sacarSobr xs n)
								etiqTrain = sacarSublista initP finP (sacarSobr ys n)
								etiqTest = sublista initP finP (sacarSobr ys n)
								initP = ((length xs) `div` n)*(p-1)
								finP = (((length xs) `div` n)*p)-1

---- Auxiliar -- Dada una cuatrupla devuelve su cuarta componente
cuartaCoordenada :: (a,b,c,d) -> d
cuartaCoordenada (_,_,_,z) = z

-- Auxiliar -- Dada una lista de cuatruplas con datos y etiquetas separados por training y validacion, 
			-- devuelve las etiquetas que devuelve nuestro modelo aplicado a cada instancia de prueba. 
			-- Ver que uso map, porque a mi modelo entrenado le paso muchas instancias, no una sola.
			-- Hardcodeamos 15 y distEuclideana porque lo dice el enunciado.
obtenerEtiquetas :: [(Datos, Datos, [Etiqueta], [Etiqueta])] -> [[Etiqueta]]
obtenerEtiquetas = map knnSobreDatosVal
					where knnSobreDatosVal = (\(dTrain,dVal,lTrain,lVal) -> (map (knn 15 dTrain lTrain distEuclideana) dVal))
									
nFoldCrossValidation :: Int -> Datos -> [Etiqueta] -> Float
nFoldCrossValidation n ds es = mean (zipWith accuracy (obtenerEtiquetas nParticionesDatos) etireales)
								where 
									nParticionesDatos = [separarDatos ds es n p | p <- [1..n]]
									etireales = map cuartaCoordenada nParticionesDatos
-- Primero, obtenemos una lista con los datos ordenados segun los de entrenamiento y los de prueba para cada particion (nParticionesDatos)
-- Luego, con obtener etiquetas entreno mis modelos y veo que etiqueta me tiran a cada prueba, luego mido el
-- porcentaje de aciertos respecto a las verdaderas etiquetas, y al final calculo el promedio.
