#!/bin/bash
string="commander_Fulltest.root "
for dir in ./*/
do
    echo $dir
    string2=$dir
    string2+="result.root"
    echo $string2
    if [ -e $string2 ];
    then 
        string+=$string2;
        string+="  ";
    fi;
done
echo $string
hadd $string
