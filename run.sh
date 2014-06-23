#!/bin/bash

# values to use in the scripted steps below
local_work_dir=../EO1-Wheel-Demo

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
 -mapper ${local_work_dir}/ClassifierMapper.py \
 -reducer NONE \
 -file ${local_work_dir}/ClassifierMapper.py \
 -file ${local_work_dir}/modules/binaryhadoop.py \
 -file ${local_work_dir}/modules/utilities.py \
 -file ${local_work_dir}/FourClassTrainingSet.txt \
 -file ${local_work_dir}/classifierconfig


exit 0



