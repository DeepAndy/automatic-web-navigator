#!/bin/bash 

if [[ $test =~ .*\.png ]]; then
    echo "TRUE"
fi

for file in $(ls images-copy/)
do
    if [[ $file =~ (.*)\.png ]]; then
        test=${BASH_REMATCH[1]}
        new_file_0="${test}_0.png"
        new_file_1="${test}_1.png"
        cp ./images/$file ./images/$new_file_0
        cp ./images/$file ./images/$new_file_1
    fi
    if [[ $file =~ (.*)\.jpg ]]; then
        test=${BASH_REMATCH[1]}
        new_file_0="${test}_0.jpg"
        new_file_1="${test}_1.jpg"
        cp ./images/$file ./images/$new_file_0
        cp ./images/$file ./images/$new_file_1
    fi
    if [[ $file =~ (.*)\.JPG ]]; then
        test=${BASH_REMATCH[1]}
        new_file_0="${test}_0.JPG"
        new_file_1="${test}_1.JPG"
        cp ./images/$file ./images/$new_file_0
        cp ./images/$file ./images/$new_file_1
    fi

done
