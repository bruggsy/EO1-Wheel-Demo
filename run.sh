#!/bin/bash

#for timing tests
#START=$(date +%s)

# values to use in the scripted steps below
local_work_dir=../EO1-Wheel-Demo
# Hadoop streaming bug workaround
libjar_dir=/home/hduser/matsu-project/analyticwheel.jobs/lib/PutToAccumulo/target
# HDFS cache used to pass around files
CACHE=hdfs://node:port

#output directory
BASE_DIR=/user/hduser/wheelTestOutput/
WORKING_DIR=${BASE_DIR}/  
hadoop fs -mkdir ${WORKING_DIR}      #make sure output directories exist
#hadoop fs -mkdir ${WORKING_DIR}/temp

MR_INPUT=$1

# Intermediate working directories
#classifier_output_dir=${WORKING_DIR}/temp/classifier-1
#mapper_output_dir=${WORKING_DIR}/mapper-1


# Output directories to keep
analyzed_image_dir=${WORKING_DIR}/classifier

hadoop dfs -rmr ${analyzed_image_dir}    #remove old output directory

################
###CLASSIFIER###

#for i in `seq 1 10`
#do

hadoop jar ${HADOOP_HOME}/contrib/streaming/hadoop-streaming-*.jar \
 -D mapred.min.split.size=10737418240 \
 -inputformat org.apache.hadoop.mapred.SequenceFileAsBinaryInputFormat \
 -input ${MR_INPUT} \
 -output ${analyzed_image_dir} \
 -mapper ${local_work_dir}/ClassifierMapper.py \
 -reducer NONE \
 -file ${local_work_dir}/ClassifierMapper.py \
 -file ${local_work_dir}/../lib/NewImageScan/src/main/python/binaryhadoop.py \
 -file ${local_work_dir}/../lib/NewImageScan/src/main/python/utilities.py \
 -file ${local_work_dir}/FourClassTrainingSet.txt \
 -file ${local_work_dir}/classifierconfig

# Clean up 
#hadoop fs -rmr -skipTrash ${WORKING_DIR}/temp

#hadoop dfs -rmr ${analyzed_image_dir}
# -file ${local_work_dir}/ClassifierReducer.py \
# -D stream.map.output=typedbytes \

# -D stream.reduce.input=typedbytes \

# -reducer ${local_work_dir}/ClassifierReducer.py \
#END=$(date +%s)
#DIFF=$(($END-$START))
#echo "run $i took $DIFF seconds" >> timelog
#done

exit 0



