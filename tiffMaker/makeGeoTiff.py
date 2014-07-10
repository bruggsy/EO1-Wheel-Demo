#!/usr/bin/env python

def compressTiff(imgData,dirName):
    base_name = str(dirName+imgData['imgName'])
    subprocess.call(['gdal_translate','-co','compress=LZW',base_name+'.tiff',base_name+'_LZW.tiff'])
    pass

def makePng(imgData,dirName):
    base_name = str(dirName+imgData['imgName'])
    subprocess.call(['gdal_translate','-of','PNG','-ot','Byte','-scale','0','5000',base_name+'.tiff',base_name+'.png'])
    pass

def createGeoTiff(imgData,dirName):
    format1 = "GTiff"
    driver = gdal.GetDriverByName(format1)
    
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
    img = np.reshape(img,shape)
    

    dst_ds.GetRasterBand(1).WriteArray(img)

    srs = None
    dst_ds = None

if __name__=="__main__":

    import gdal, osr, ogr
    import argparse
    import json
    import numpy as np
    import subprocess

    parser = argparse.ArgumentParser(description='Create referenced GeoTiff from wheel Output')
    parser.add_argument('inLoc',type=str,help='Location of wheel output to be read in')
    parser.add_argument('outDir',type=str,help='Directory to output files to')
    
    options = parser.parse_args()
    sceneJSON = options.inLoc
    outFile = options.outDir

    imgData = json.load(open(sceneJSON))
    
    dirName = outFile+imgData['imgName'][0:-8]+"/"

    subprocess.call(['mkdir','-p',dirName])

    createGeoTiff(imgData,dirName)
    compressTiff(imgData,dirName)
    makePng(imgData,dirName)
    pass
