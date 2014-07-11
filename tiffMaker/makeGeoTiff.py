#!/usr/bin/env python

'''
ABOUT:
This Python program will create a georeferenced geoTiff, given 
a certain JSON structure (detailed in documentation) and a
target directory. Can create .pngs and compressed tiffs as well (not enabled).

DEPENDS:
ogr
gdal
osr
numpy
argparse
subprocess

AUTHORS:
Jake Bruggemann

HISTORY:
July 2014: Original script (beta).

USE:
For use on the Open Science Data Cloud public data commons.
> python makeRGB.py INPUT OUT_DIRECTORY NUMBER_BANDS [COLORFILE]
For example, make a two-band tiff from a JSON loaded into EO1A1930292014029110PZ.json and target directory images/, with color file color.txt:
> python makeGeoTiff.py EO1A1930292014029110PZ.json images/ 2 color.txt
'''

__author__ = "Jake Bruggemann"
__version__ = 0.1

#Creates compessed tiff
def compressTiff(imgData,dirName):
    base_name = str(dirName+imgData['imgName'])
    subprocess.call(['gdal_translate','-co','compress=LZW',base_name+'.tiff',base_name+'_LZW.tiff'])
    pass

def makePng(imgData,dirName):
    base_name = str(dirName+imgData['imgName'])
    subprocess.call(['gdal_translate','-of','PNG','-ot','Byte','-scale','0','5000',base_name+'.tiff',base_name+'.png'])
    pass

def createColorTiff(imgData,dirName,colorFile):
    base_name = str(dirName+imgData['imgName'])
    subprocess.call(['gdaldem','color-relief','-alpha',base_name+'.tiff',colorFile,base_name+'_COLOR.tiff'])
    pass

def createGeoTiff(imgData,dirName,numRast):
    format1 = "GTiff"
    driver = gdal.GetDriverByName(format1)

    try:
        shape = imgData['imgShape']
        sceneName = imgData['imgName']
        
        base_name = str(dirName+imgData['imgName'])
        
        dst_ds = driver.Create(base_name+'.tiff',shape[1],shape[0],1,gdal.GDT_Byte)
        dst_ds.SetGeoTransform(imgData['geoTrans'])
        srs = osr.SpatialReference()
        
        northSouth = (imgData['UTM'][-1] == 'N')
        srs.SetUTM(int(imgData['UTM'][0:-1]),northSouth)
        
        srs.SetWellKnownGeogCS('WGS'+str(imgData['WGS']))
        dst_ds.SetProjection(srs.ExportToWkt())
        
        img = np.array([imgData['img']])
        print shape
        img = np.reshape(img,shape+[1])  #Just to make sure array is 3-D with right shape
    except KeyError:
        print "Keys missing from JSON: Current keys are:"
        print imgData.keys()
        return False
    
    for i in np.arange(numRast):
        bandNum = int(i+1)
        dst_ds.GetRasterBand(bandNum).WriteArray(img[:,:,i])
        
    srs = None
    dst_ds = None
    return True

#######################################
#######################################

if __name__=="__main__":

    import gdal, osr, ogr
    import argparse
    import json
    import numpy as np
    import subprocess

    parser = argparse.ArgumentParser(description='Create referenced GeoTiff from wheel Output')
    parser.add_argument('inLoc',type=str,help='Location of wheel output to be read in')
    parser.add_argument('outDir',type=str,help='Directory to output files to')
    parser.add_argument('numRast',type=int,help='Number of raster bands')
    parser.add_argument('colorFile',nargs='?',const=None,type=str,default=None,help='Color file to create colored tiffs (Default None)')


    options = parser.parse_args()
    sceneJSON = options.inLoc
    outFile = options.outDir
    numRast = options.numRast
    colorFile = options.colorFile

    imgData = json.load(open(sceneJSON))
    
    dirName = outFile+imgData['imgName'][0:-8]+"/"

    subprocess.call(['mkdir','-p',dirName])

    SUCCESS = createGeoTiff(imgData,dirName,numRast)
    if SUCCESS: #Can add png maker, compresser here
        if colorFile != None:
            createColorTiff(imgData,dirName,colorFile)
    pass
