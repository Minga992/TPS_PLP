#!/bin/bash

USO="Use \t SLSParser [-o SALIDA] [-c ENTRADA | FUENTE]"
OUTPUT=1

if [ "$#" -eq 1 ]; then
	SALIDA=$(>&1)
	FUENTE="$1"
elif [ "$#" -eq 2 ]; then
	if [ "$1" != "-c" ]; then
		echo "$USO"
	else
		SALIDA=$(>&1)
		FUENTE=$(<"$2")
	fi
elif [ "$#" -eq 3 ]; then
	if [ "$1" != "-o" ]; then
		echo "$USO"
	else
		SALIDA="$2"
		FUENTE="$3"
		OUTPUT=2
	fi
elif [ "$#" -eq 4 ]; then
	if [ "$1" != "-o" ]; then
		echo "$USO"
	elif [ "$3" != "-c" ]; then
		echo "$USO"
	else
		SALIDA="$2"
		FUENTE=$(<"$4")
		OUTPUT=2
	fi
else
    echo "Illegal number of parameters\n"
    echo "$USO"
    exit
fi
    

if [ $OUTPUT == 1 ]; then
	python parser.py "$FUENTE"
else
	python parser.py "$FUENTE" 1>$SALIDA
fi

exit
