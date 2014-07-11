#!/bin/bash

# ABOUT:
# This shell script sets up and runs a miniature version of the Matsu wheel
# It has one analytic, an SVM classifer for terrain types.
# As input it takes the directory of .seqpngs (sequential pngs) to be
# loaded from HDFS
# As output it creates georeferenced GeoTiffs.
#
# AUTHORS:
# Jake Bruggemann
#
# HISTORY:
# July 2014: Original Script (beta)
#
# USE:
# For use in Open Science Data Cloud mini-wheel Demo
# > ./run.sh HDFS_DIRECTORY
# For example, run on files stored in /user/hduser/input/
# > ./run.sh /user/hduser/input/

# values to use in the scripted steps below
local_work_dir=../EO1-Wheel-Mini

# HDFS cache used to pass around files
CACHE=hdfs://node:port

#output directory
BASE_DIR=/user/hduser/wheelTestOutput/
WORKING_DIR=${BASE_DIR}/  
hadoop fs -mkdir ${WORKING_DIR}      #make sure output directories exist

# Location of input data
MR_INPUT=$1


# Output directory
analyzed_image_dir=${WORKING_DIR}/classifier

hadoop dfs -rmr ${analyzed_image_dir}    #remove old output directory

################
###CLASSIFIER###


hadoop jar ${HADOOP_HOME}/contrib/streaming/hadoop-streaming-*.jar \
 -D mapred.min.split.size=10737418240 \
 -inputformat org.apache.hadoop.mapred.SequenceFileAsBinaryInputFormat \
 -input ${MR_INPUT} \
 -output ${analyzed_image_dir} \
 -mapper ${local_work_dir}/classifier/ClassifierMapper.py \
 -reducer NONE \
 -file ${local_work_dir}/classifier/ClassifierMapper.py \
 -file ${local_work_dir}/modules/binaryhadoop.py \
 -file ${local_work_dir}/modules/utilities.py \
 -file ${local_work_dir}/modules/geoReference.py \
 -file ${local_work_dir}/classifier/FourClassTrainingSet.txt \
 -file ${local_work_dir}/classifier/classifierconfig



./tiffMaker/wheelRead.sh ${analyzed_image_dir} classImgs/

exit 0
