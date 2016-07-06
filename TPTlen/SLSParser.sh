#!/bin/bash

USO="Use \t SLSParser [-o SALIDA] [-c ENTRADA | FUENTE]"

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
		SALIDA=$(>"$2")
		FUENTE="$3"
	fi
elif [ "$#" -eq 4 ]; then
	if [ "$1" != "-o" ]; then
		echo "$USO"
	elif [ "$3" != "-c" ]; then
		echo "$USO"
	else
		SALIDA=$(>"$2")
		FUENTE=$(<"$4")
	fi
else
    echo "Illegal number of parameters\n"
    echo "$USO"
    exit
fi
    
python parser.py "$FUENTE" "$SALIDA"

exit