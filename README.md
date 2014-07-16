# OSDC Matsu Wheel EO1 Demo

Hello! Welcome to the Open Science Data Cloud's demo on the Matsu Wheel.
In this tutorial, we will show you how to use the OSDC wheel to run 
analytics over a dataset.  For this demo, we'll show you how to run a
simple support vector machine algorithm over the NASA EO1 dataset. 

Much of the code in this tutorial is derived from the OSDC EO1 Data Tutorial, which
covers a similar method of image classification, but without using a Hadoop system.
It can be accessed [here](https://github.com/mtpatter/eo1-demo "EO1-Demo").

The files contained in this demo are as follows:
* classifier/: Directory containing files for classifier
  * ClassifierMapper.py: Mapper function for wheel streaming
  * classifierconfig: configuration file
  * FourClassTrainingSet.txt: csv file containing training data
* modules/: Diretory containing modules for binaryhadoop and reading sequence files
* tiffMaker/: Directory containing files for creating GeoTiffs from wheel output
  * wheelReader.sh: Reads and formats wheel output
  * makeGeoTiff.py: Creates georeferenced GeoTiffs
* testImage/: folder containing images for testing wheel
* run.sh: shell script for running wheel

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
$ hadoop dfs -copyFromLocal testImage/* /user/hduser/wheelTest/
```
Check what's in the directory again, you should see the contents of testImage listed. Now we can run the wheel. 
The wheel consists of a series of MapReduce jobs, where the necessary data is streamed through the jobs and the analytics are
spit out at the end, written into Accumulo. In our case, we only have one MapReduce job and are writing the results back into HDFS.

An individual MapReduce job has three steps: Map, Shuffle & Sort, and Reduce. In a very paraphrased fashion, they do the following:

Mapper:         Read and sort data, convert into key - value pairs for reducer.

Shuffle & Sort: Sort output from mapper by key

Reduce:         Read in key-value pairs and run operation on them grouped by key, output to HDFS.

In our case, the .seqpng files that we uploaded into HDFS already come in key-value form, so we'll only 
use a mapper, which will read in the .seqpng's and apply the classifier to them. Seqpngs are binary sequential files
corresponding to individual scenes where each line is ordered into key-value pairs.
The keys in these .seqpng's correspond to the mask, metadata, or individual band of the scene. In the mapper we reconstruct
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

The classifier is built to be fault tolerant and automatically determine if each scene is ALI or Hyperion. It will issue warnings if some bands are missing from the dataset.
 These can be checked in the hadoop logs. As hduser, cd into ```/usr/local/hadoop/logs/userlogs/```. If you ```ls``` here, you will see folders labelled similarily to
```
job_201406041059_0199
```
These correspond to the job ID's of the hadoop MR job you just ran. You can check the output stream for the ID of your specific job. In the folder
for your job, you will see something like this:
```
attempt_201406231547_0168_m_000000_0  attempt_201406231547_0168_m_000001_0  attempt_201406231547_0168_m_000002_0  job-acls.xml
```
These correspond to the separate attempts to complete the map job on a separate file in  your data. Don't worry about how many there are exactly, 
MapReduce sometimes takes a couple of attempts to complete successfully. Go into any one and open the file ```stderr``` to see information
on your job. Here, you can see the bands that were read in, what ratios were used, and the scene ID of the scene the attempt correspond to. 

Once you're confident your job ran as you wanted it to, it's time to check what you made. 
In this example, the output for the job is simply a JSON containing all the image and georeferencing information. Let's 
check the output of the mapper by typing:
```
$ hadoop dfs -ls /user/hduser/wheelTestOutput/classifier/
```

You should see something like the following:
```
Found 3 items
-rw-r--r--   1 hduser supergroup          0 2014-07-10 17:48 /user/hduser/wheelTestOutput/classifier/_SUCCESS
drwxr-xr-x   - hduser supergroup          0 2014-07-10 17:42 /user/hduser/wheelTestOutput/classifier/_logs
-rw-r--r--   1 hduser supergroup   34993316 2014-07-10 17:42 /user/hduser/wheelTestOutput/classifier/part-00000
```

The ```_SUCCESS``` file means that the job completed succesfully. The ```part-``` is your mapper output. You have one for each mapper that ran,
in this case you should have two. The run script also converts these JSONs stored in HDFS to georeferenced GeoTiffs and PNGS. You can view
these files in the newly created classImgs directory. Each scene has its own subdirectory. In each, you can see two files, both GeoTiffs. The one
with the name ```SCENEID_CLASSIFIED.tiff``` is the classified GeoTiff, where each pixel has a value corresponding to its classified terrain type. 
The one with the name ```SCENEID_CLASSIFIED_COLOR.tiff``` is a false color RGBA GeoTiff of the classified scene
where each color corresponds to a certain terrain type.
 You can check the geogreferencing information of any of the images by using gdalinfo:

```
gdalinfo <file>
```

Using this demo and looking at the example code, you can build your own analytics that create georeferenced geoTiffs and pngs. The simple requirements
are that the MapReduce job produces a JSON with the following keys:
* UTM : UTM zone number for the scene, see function ```getUTM``` in geoReference.py
* geoTrans: Geo-Transformation vector, see function ```makeGeoTrans``` in geoReference.py
* WGS : WGS world geodetic system version number, see function ```getWGS``` in geoReference.py
* imgShape : Dimensions of scene image, numpy array in format ```[#rows, #columns]```
* imgName : Scene ID, taken from metadata under key ```originalDirName```
* img: Raster image created from, 2-D numpy array converted to list.

Using this demo and the documentation for each function, hopefully you can create your own analytics and plug them into the wheel! Happy rolling!
