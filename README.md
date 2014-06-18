# OSDC Matsu Wheel EO1 Demo

Hello! Welcome to the Open Science Data Cloud's demo on the Matsu Wheel.
In this tutorial, we will show you how to use the OSDC wheel to run 
analytics over a dataset. For this demo, we'll show you how to run a
simple support vector machine algorithm over the NASA EO1 dataset.

The files contained in this demo are as follows:
* ClassifierMapper.py: Mapper function for wheel streaming
* run.sh: shell script for running wheel
* classifierconfig: configuration file
* FourClassTrainingSet.txt: csv file containing training data
* testImages/: folder containing images for testing wheel

In order to use the HDFS system, you must be logged in as the hadoop user. In a separate terminal window, type in
```
$ su - hduser
```

Ubuntu will then ask you for a password. In this case, the password is: Puppies

Your home directory now holds all the files you need to use the wheel. Before we can do that, however, we need to boot 
up HDFS. In the terminal, type:
```
$ /usr/local/hadoop/bin/start-all.sh
```

This will start up HDFS. Once this is complete you can check that all the nodes are up by typing ```jps``` into the terminal.
You should get output that looks something like this:
```
30996 NameNode
31149 DataNode
4271 Jps
31450 JobTracker
31331 SecondaryNameNode
31609 TaskTracker
```
Your numbers might be different, but all of the nodes should be listed. Now, we can check what's stored in HDFS. Into the terminal, type
```
$ hadoop dfs -ls
```
and see what's been stored. You should see a directory called ```/user/hduser/wheelTest/```, check what's in there using:
```
$ hadoop dfs -ls /user/hduser/wheelTest/
```

Hm, nothing in there. Let's put some files in it to test. In the terminal, type in:
```
$ hadoop dfs -copyFromLocal testImages/* /user/hduser/wheelTest/
```
Check what's in the directory again, you should see the contents of testImages listed. Now we can run the wheel. 
The wheel consists of a series of MapReduce jobs, where the necessary data is streamed through the jobs and the analytics are
spit out at the end, written into Accumulo. In our case, we only have one MapReduce job and are writing the results back into HDFS.

An individual MapReduce job has three steps: Map, Shuffle & Sort, and Reduce. In a very paraphrased fashion, they do the following:

Mapper:         Read and sort data, convert into key - value pairs for reducer.

Shuffle & Sort: Sort output from mapper by key

Reduce:         Read in key-value pairs and run operation on them grouped by key, output to HDFS.

In our case, the .seqpng files that we uploaded into HDFS already come in key-value form, so we'll only 
use a mapper, which will read in the .seqpng's and apply the classifier to them. Seqpngs are binary sequential files
where each line is ordered in the following fashion
```
key	value
```

