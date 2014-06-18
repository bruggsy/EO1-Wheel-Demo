# OSDC Matsu Wheel EO1 Demo

Hello! Welcome to the Open Science Data Cloud's demo on the Matsu Wheel
In this tutorial, we will show you how to use the OSDC wheel to run 
analytics over a dataset. For this demo, we'll show you how to run a
simple support vector machine algorithm over the NASA EO1 dataset.

The files contained in this demo are as follows:
* ClassifierMapper.py: Mapper function for wheel streaming
* run.sh: shell script for running wheel
* classifierconfig: configuration file
* FourClassTrainingSet.txt: csv file containing training data

In order to use the HDFS system, you must be logged in as the hadoop user. In a separate terminal window, type in
```
su - hduser
```

Ubuntu will then ask you for a password. In this case, the password is: Puppies

Your home directory now holds all the files you need to use the wheel. Before we can do that, however, we need to boot 
up HDFS. In the terminal, type:
```
/usr/local/hadoop/bin/start-all.sh
```

