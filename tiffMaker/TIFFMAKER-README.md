# OSDC Matsu Wheel EO1 Demo - tiffMaker

Here is a short description of the contents of the ```tiffMaker``` folder for the
OSDC Matsu Wheel EO1 Demo. This folder contains four files:
* TIFFMAKER-README.md: file you are currently reading.
* color.txt: Space delimited text file containing information for creating colored .geoTiff's.
* makeGeoTiff.py: Python script for creating georeferenced .geoTiff's from JSON's created by wheelRead.sh
* wheelRead.sh: Shell script for reading MapReduce output from HDFS and copying to local file system, calls makeGeoTiff.py to save geoTiffs locally.

Here is some additional information for some of the files:

## color.txt
Space delimited file for creating colored .geoTiff's. Each line corresponds to a possible
value of a pixel in the .geoTiff, and then gives that value a correspond Red-Green-Blue-Alpha
 color scheme.
The format is as follows:
```
pixel_value red green blue alpha
```

