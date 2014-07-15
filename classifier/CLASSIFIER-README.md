# OSDC Matsu Wheel EO1 Demo - classifier

Here is a short description of the contents of the ```classifier``` folder for the 
OSDC Matsu Wheel EO1 Demo. This folder contains four files:
* CLASSIFIER-README.md: file you are currently reading
* ClassifierMapper.py: Python script that acts a Mapper for a Hadoop MapReduce job
* FourClassTrainingSet.csv: Comma separated file containing training data for SVM classifier
* classifierconfig.tsv: Tab separated file containing configuration information

Here's some further explanation of some of the files:

## FourClassTrainingSet.csv
   Training data manually constructed from Hyperion Data. Contains all reflectance values 
for all Hyperion bands and associated terrain type.

## classifierconfig.tsv
Contains configuration options for Support Vector Machine classifier. Options are as follows, taken from [sklearn documentation](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html "Documentation"):
* classifier.kernel: kernel type to be used for algorithm. Can be one of: linear, poly, rbf, sigmoid, or precomputed. 
* classifier.C: Penalty parameter C for the error term.
* classifier.gamma: Kernel coefficient for rbf, poly and sigmoid. If gamma is 0.0 then 1/n_features will be used instead.
* ratio: Ratio of ALI or approximate ALI bands to be used as further dimensions for SVM algorithm. Structure is as follows: ```ratio   numerator_band    denomination_band```