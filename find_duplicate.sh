#!/bin/bash

#Hazel Court
PATH=/bin:/usr/bin
#find_duplicate finds duplicate files in the given directory and its sub directories
dir=$1
if [[ ! -d $dir ]]
then
    echo "$dir is not a directory."
    exit 1
fi
find $dir -type f | xargs md5sum | sort |
awk '
    BEGIN {FS=" "}
    {if ($1==old1)
        print ($2," duplicate of ",old2)
    else
        {
        old1=$1;
        old2=$2;
        }
    }
'

exit 0