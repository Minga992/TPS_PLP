-- Para correr los tests:
-- ghc Tests-alu.hs && ./Tests-alu

import Tp
import Test.HUnit
import Data.List

-- evaluar main para correr todos los tests
main = runTestTT allTests

allTests = test [
 	"split" ~: testsSplit,
 	"longitudPromedioPalabras" ~: testsLongitudPromedioPalabras,
 	"cuentas" ~: testsCuentas,
 	"repeticionesPromedio" ~: testRepeticionesPromedio,
 	"frecuenciaTokens" ~: testsFrecuenciaTokens,
 	"normalizarExtractor" ~: testsNormalizarExtractor,
 	"extraerFeatures" ~: testsExtraerFeatures,
 	"distancias" ~: testsDistancias,
 	"knn" ~: testsKnn,
 	"separarDatos" ~: testsSepararDatos,
 	"accuracy" ~: testsAccuracy,
 	"nFoldCrossValidation" ~: testsNFoldCrossValidation
 	]

testsSplit = test [
 	split ',' ",PLP," ~?= ["PLP"],
 	split ',' " ,PLP, " ~?= [" ","PLP"," "],
 	split ',' ",,,,,,," ~?= [],
 	split ',' ",,,PLP,,,,,PLP,,," ~?= ["PLP","PLP"]
  	]

testsLongitudPromedioPalabras = test [
	longitudPromedioPalabras "Este es el test donde testeo cuál es la longitud promedio de las palabras" ~?= 4.285714
	]

testsCuentas = test [
	cuentas ["x","x","y","x","z"] ~?= [(3,"x"), (1,"y"), (1,"z")],
	cuentas ["a","b","r","a","c","a","d","a","b","r","a"] ~?= [(5,"a"),(2,"b"),(2,"r"),(1,"c"),(1,"d")]
	]

testRepeticionesPromedio = test [
	repeticionesPromedio "cabal transformers 0.4 error transformers 0.4 error 0.4 error error cabal tuvieja" ~?= 2.4
	]
	
testsFrecuenciaTokens = test [
	(head frecuenciaTokens) "use_snake_case !" ~?= 0.125, -- esto es con el _
	(frecuenciaTokens !!23) "use_snake_case !" ~?= 0.0625, -- esto es con el !
	(frecuenciaTokens !!4) "use_snake_case !" ~?= 0 -- esto es con el *
	]

testsNormalizarExtractor = 
	let
		xs = ["soy una papa","ale es una papa","todos somos papas"]
		ys = ["soy una papa!","ale es una papa!!","todos somos papas!!!"]
	in
	test [
		normalizarExtractor xs longitudPromedioPalabras "soy una papa" ~?= 0.6666666,
		normalizarExtractor xs repeticionesPromedio "ale es una papa" ~?= 1,
		map (normalizarExtractor ys (frecuenciaTokens !!23)) ys ~?= [0.5128205,0.7843137,1]
	]

testsExtraerFeatures = test [
	let ps = ["anita lava la tina","dabale arroz a la zorra el abad","saben que sabemos que saben esto"] in
	extraerFeatures [longitudPromedioPalabras,repeticionesPromedio] ps ~?= [[0.8333333,0.6666667],[0.7936508,0.6666667],[1,1]],
	let ts = ["b=a", "a = 2; a = 4", "C:/DOS C:/DOS/RUN RUN/DOS/RUN"] in
	extraerFeatures [longitudPromedioPalabras, repeticionesPromedio] ts ~?= [[0.33333334,0.6666667],[0.12962963,1.0],[1.0,0.6666667]]
	]

testsDistancias = test [
	distEuclideana [1.0,0.75,0.8125] [0.75,1.0,0.5] ~?= 0.47186464,
	distCoseno [0,3,4] [0,-3,-4] ~?= -1.0
	]

testsKnn = test [
--	No hacemos caso especial al hecho de que [1,1] esta dentro de los datos iniciales.
	(knn 2 [[0,1],[0,2],[2,1],[1,1],[2,3]] ["i","i","f","f","i"] distEuclideana) [1,1] ~?= "f",
	(knn 3 [[0,1],[0,2],[2,1],[1,1],[2,3]] ["i","i","f","f","i"] distEuclideana) [1,1] ~?= "f"
	]

testsSepararDatos = 
	let 
		xs = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]] :: Datos
		y = ["1","2","3","4","5","6","7"]
	in
	test [
		separarDatos xs y 3 2 ~?= ([[1.0,1.0],[2.0,2.0],[5.0,5.0],[6.0,6.0]],[[3.0,3.0],[4.0,4.0]],["1","2","5","6"],["3","4"]),
		separarDatos xs y 7 2 ~?= ([[1.0,1.0],[3.0,3.0],[4.0,4.0],[5.0,5.0],[6.0,6.0],[7.0,7.0]],[[2.0,2.0]],["1","3","4","5","6","7"],["2"])
	]

testsAccuracy = test [
	accuracy ["f", "f", "i", "i", "f"] ["i", "f", "i", "f", "f"] ~?= 0.6
	]

testsNFoldCrossValidation = test [
--	Esta prueba funciona pero en realidad los datos van a estar normalizados
	nFoldCrossValidation 2 [[2,1],[2,2],[4,3],[3,2]] ["f","i","f","i"] ~?= 0.5,
--	Aca probamos con datos normalizados
	let
		ds = [[0.05,0.05],[0.1,0.1],[0.15,0.15],[0.2,0.2],[0.25,0.25],[0.3,0.3],[0.35,0.35],[0.4,0.4],[0.45,0.45],[0.5,0.5],[0.55,0.55],[0.6,0.6],[0.65,0.65],[0.7,0.7],[0.75,0.75],[0.8,0.8],[0.85,0.85],[0.9,0.9],[0.95,0.95],[1.0,1.0]]
		ls = ["f", "f", "i", "i", "f", "i", "f", "i", "f", "f", "f", "f", "i", "i", "f", "i", "f", "i", "f", "f"]
	in
		nFoldCrossValidation 20 ds ls ~?= 0.55
	]
