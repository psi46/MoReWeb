#!/bin/bash
args=("$@")
echo 'ARGUMENTS: ',${args}
string="$args/commander_Fulltest.root "
echo 'STRING: ',$string
#for dir in ./*/
n=0
for dir in ${args}/*/
do
    echo $dir
    string2=$dir
    string2+="result.root"
    echo $string2
    if [ -e $string2 ];
    then 
        string+=$string2;
        string+="  ";
        ((n = n+1))
    fi;
done
echo 'Found: ',$n
if (($n >= 1))
then
    echo 'ANALYZE'
    hadd -f $string
else
    echo 'DO NOT Analyze since there are no files'
fi
echo 'String', $string
exit
