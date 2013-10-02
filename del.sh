#!/bin/bash

if [[ "$1" != "--list" && "$1" != "--empty" ]]
then
    mv $1 ~/trash
fi
if [[ "$1" == "--list" || "$2" == "--list" || "$3" == "--list" ]]
then
    ls ~/trash
fi
if [[ "$1" == "--empty" || "$2" == "--empty" || "$3" == "--empty" ]]
then
    for f in $(ls ~/trash)
    do
        rm ~/trash/"$f"
    done
fi

exit 0