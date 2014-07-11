#!/bin/bash


#ABOUT:
#This shell script will read in the HDFS output from a wheel classification,
#sort it into individual scenes, and then create geoTiffs with the classification.

#AUTHORS:
#Jake Bruggemann

#HISTORY:
#July 2014: Original script (beta).

#USE:
#For use on the Open Science Data Cloud public data commons.
#> ./wheelRead.sh MR_OUTPUT OUT_DIR
#For example, read in output stored on HDFS in /user/hduser/output and write geoTiffs to geoImgs/
#> ./wheelRead.sh /user/hduser/output/ geoImgs/


CURRENT_DIR=tiffMaker

MR_OUTPUT=$1
OUT_DIR=$2


mkdir -p ${OUT_DIR}
mkdir -p tmp

hadoop dfs -ls ${MR_OUTPUT}/part* > tmp/ls

subLine=part

for line in $(cat tmp/ls)
do
    if [[ "$line" =~ "part" ]]; then
	echo $line >> tmp/fileList
    fi	
done

for line in $(cat tmp/fileList)
do
    hadoop dfs -cat $line > tmp/json
    python ${CURRENT_DIR}/makeGeoTiff.py tmp/json ${OUT_DIR} 1 ${CURRENT_DIR}/color.txt
done

rm -r tmp