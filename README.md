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

Once you're logged in, cd into the EO1-Wheel-Demo directory. 

You now can see all the files you need to use the wheel. Before we can do that, however, we need to boot 
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
corresponding to individual scenes where each line is ordered into key-value pairs.

and each of these lines corresponds to the mask, metadata, or individual band of the scene. In the mapper we reconstruct
the image line-by-line from the .seqpng, and from there run the classifier on it. The classifier is run using the command:
```
$ ./run.sh /user/hduser/wheelTest/
```

You should see something like the following being printed out:
```
Deleted hdfs://localhost:54310/user/hduser/wheelTestOutput/classifier
packageJobJar: [../classifier/ClassifierMapper.py, ../classifier/../lib/NewImageScan/src/main/python/binaryhadoop.py, ../classifier/../lib/NewImageScan/src/main/python/utilities.py, ../classifier/FourClassTrainingSet.txt, ../classifier/classifierconfig, /app/hadoop/tmp/hadoop-unjar457409916355964329/] [] /tmp/streamjob6986399193070302753.jar tmpDir=null
14/06/18 18:09:28 INFO mapred.FileInputFormat: Total input paths to process : 2
14/06/18 18:09:28 INFO streaming.StreamJob: getLocalDirs(): [/app/hadoop/tmp/mapred/local]
14/06/18 18:09:28 INFO streaming.StreamJob: Running job: job_201406041059_0199
14/06/18 18:09:28 INFO streaming.StreamJob: To kill this job, run:
14/06/18 18:09:28 INFO streaming.StreamJob: /usr/local/hadoop/libexec/../bin/hadoop job  -Dmapred.job.tracker=localhost:54311 -kill job_201406041059_0199
14/06/18 18:09:28 INFO streaming.StreamJob: Tracking URL: http://localhost:50030/jobdetails.jsp?jobid=job_201406041059_0199
14/06/18 18:09:29 INFO streaming.StreamJob:  map 0%  reduce 0%
14/06/18 18:09:46 INFO streaming.StreamJob:  map 68%  reduce 0%
14/06/18 18:09:49 INFO streaming.StreamJob:  map 78%  reduce 0%
14/06/18 18:09:52 INFO streaming.StreamJob:  map 88%  reduce 0%
14/06/18 18:09:55 INFO streaming.StreamJob:  map 98%  reduce 0%
14/06/18 18:09:58 INFO streaming.StreamJob:  map 100%  reduce 0%
14/06/18 18:14:46 INFO streaming.StreamJob:  map 100%  reduce 100%
14/06/18 18:14:46 INFO streaming.StreamJob: Job complete: job_201406041059_0199
14/06/18 18:14:46 INFO streaming.StreamJob: Output: /user/hduser/wheelTestOutput///classifier
```
In this example, the output for the job is simply a counter for the different terrain types labelled in the scene. Let's 
check the output of the mapper by typing:
```
$ hadoop dfs -ls /user/hduser/wheelTestOutput/classifier/
```
You'll see that the output comes in separate files as 'part-*'. This corresponds to the output from each separate mapper - usually one for each file.
You can look at the output for all the files with the command:
```
$ hadoop dfs -cat /user/hduser/wheelTestOutput/classifier/part*
```

There are the amounts of terrain of each type that your classifier found. By looking in the run.sh and ClassifierMapper.py files you can
design your own analytics and plug them into the wheel! Happy rolling!