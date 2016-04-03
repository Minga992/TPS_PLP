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

--Verision explicita:
--split d [] = []
--split d xs = takeWhile (\= d) xs : (split d tail(dropWhile (\= d) xs))

--split d [] = [[]]
--split d (x:xs) = if d == x then []:split(xs)
--       				   	else (x:head(split(xs))):tail(split(xs))

--Version final
split d = foldr (\x (xs:xss) -> if x == d then []:xs:xss else (x:xs):xss) [[]]
-- si me encuentro con un delimitador, es una palabra aparte.  Si no, la letra es parte de la misma palabra.


longitudPromedioPalabras :: Extractor
longitudPromedioPalabras xs = mean map genericLength split " " xs
-- Sin los parentesis se ve horrible, pero la idea es, hago el split sacando los espacios del medio, eso me da una lista de listas,
-- le aplico map con genericLength, que dada una lista te devuelve su longitud en algun formato(supongo que es adaptable o algo asi,
-- o sino no entendi) y a eso le aplico mean que es una suerte de promedio.


cuentas :: Eq a => [a] -> [(Int, a)]

--Version explicita:
--cuentas [] 	 = []
--cuentas (x:xs) = (genericLength filter (= x) x:xs) : cuentas filter (\= x) x:xs

--se podria haber hecho con head, pero me parecio mas claro asi
cuentas = undefined

repeticionesPromedio :: Extractor
repeticionesPromedio = undefined

tokens :: [Char]
tokens = "_,)(*;-=>/.{}\"&:+#[]<|%!\'@?~^$` abcdefghijklmnopqrstuvwxyz0123456789"

frecuenciaTokens :: [Extractor]
frecuenciaTokens = undefined

normalizarExtractor :: [Texto] -> Extractor -> Extractor
normalizarExtractor = undefined

extraerFeatures :: [Extractor] -> [Texto] -> Datos
extraerFeatures = undefined

distEuclideana :: Medida
distEuclideana = undefined

distCoseno :: Medida
distCoseno = undefined

knn :: Int -> Datos -> [Etiqueta] -> Medida -> Modelo
knn = undefined

accuracy :: [Etiqueta] -> [Etiqueta] -> Float
accuracy = undefined

separarDatos :: Datos -> [Etiqueta] -> Int -> Int -> (Datos, Datos, [Etiqueta], [Etiqueta])
separarDatos = undefined

nFoldCrossValidation :: Int -> Datos -> [Etiqueta] -> Float
nFoldCrossValidation = undefined
