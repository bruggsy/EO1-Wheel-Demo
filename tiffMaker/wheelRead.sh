#!/bin/bash

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
    python ${CURRENT_DIR}/makeGeoTiff.py tmp/json ${OUT_DIR}
done

rm -r tmp