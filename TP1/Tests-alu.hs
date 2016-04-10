-- Para correr los tests:
-- ghc Tests-alu.hs && ./Tests-alu

import Tp
import Test.HUnit
import Data.List

-- evaluar main para correr todos los tests
main = runTestTT allTests

allTests = test [
 	"split" ~: testsSplit,
 	"cuentas" ~: testsCuentas,
 	"longitudPromedioPalabras" ~: testsLongitudPromedioPalabras,
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
 	split ',' " ,PLP, " ~?= [" ","PLP"," "]
  	]

testsCuentas = test [
--	cuentas ["x","x","y","x","z"] ~?= [(3,"x"), (1,"y"), (1,"z")]
	cuentas ["x","x","y","x","z"] ~?= [(1,"y"), (3,"x"), (1,"z")]
	
	]

testsLongitudPromedioPalabras = test [
	longitudPromedioPalabras "Este es el test donde testeo cuàl es la longitud promedio de las palabras" ~?= 4.285714
	]

testRepeticionesPromedio = test [
	repeticionesPromedio "cabal transformers 0.4 error transformers 0.4 error 0.4 error error cabal tuvieja" ~?= 2.4
	]
	
testsFrecuenciaTokens = test [
	(head frecuenciaTokens) "use_snake_case !" ~?= 0.125
	]

testsNormalizarExtractor = test [
	normalizarExtractor ["soy una papa","ale es una papa","todos somos papas"] longitudPromedioPalabras "soy una papa" ~?= 0.6666666
	]

testsExtraerFeatures = test [
	-- extraerFeatures [longitudPromedioPalabras,repeticionesPromedio] ["anita lava la tina","dabale arroz a la zorra el abad","saben que sabemos que saben esto"] ~?=
	let ts = ["b=a", "a = 2; a = 4", "C:/DOS C:/DOS/RUN RUN/DOS/RUN"] in
	extraerFeatures [longitudPromedioPalabras, repeticionesPromedio] ts ~?= [[0.33333334,0.6666667],[0.12962963,1.0],[1.0,0.6666667]]
	]

testsDistancias = test [
	distEuclideana [1.0,0.75,0.8125] [0.75,1.0,0.5] ~?= 0.47186464,
	distCoseno [0,3,4] [0,-3,-4] ~?= -1.0
	]

testsKnn = test [
	(knn 3 [[0,1],[0,2],[2,1],[1,1],[2,3]] ["i","i","f","f","i"] distEuclideana) [1,1] ~?= "f"
	]

testsSepararDatos = test [
	let 
		xs = [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]] :: Datos
		y = ["1","2","3","4","5","6","7"]
	in
	separarDatos xs y 3 2 ~?= ([[1.0,1.0],[2.0,2.0],[5.0,5.0],[6.0,6.0]],[[3.0,3.0],[4.0,4.0]],["1","2","5","6"],["3","4"])
	]

testsAccuracy = test [
	accuracy ["f", "f", "i", "i", "f"] ["i", "f", "i", "f", "f"] ~?= 0.6
	]

testsNFoldCrossValidation = test [
	nFoldCrossValidation 2 [[2,1],[2,2],[4,3],[3,2]] ["f","i","f","i"] ~?= 0.5
	]
