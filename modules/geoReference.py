#!/user/bin/env python

import gdal, osr, ogr
import numpy


def makeGeoTrans(metadata,shape):

    epsgNum = getEPSG(metadata)

    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    
    target = osr.SpatialReference()
    target.ImportFromEPSG(int(epsgNum))
    
    botLeft = metadata['registration']['bottom-left']
    upRight = metadata['registration']['top-right']
    
    blLat = botLeft['lat']
    blLng = botLeft['lng']
    urLat = upRight['lat']
    urLng = upRight['lng']

    transform = osr.CoordinateTransformation(source,target)

    blPoint = ogr.CreateGeometryFromWkt("POINT ("+str(blLat)+ " " + str(blLng) +")")
    urPoint = ogr.CreateGeometryFromWkt("POINT ("+str(urLat)+ " " + str(urLng) +")")

    blPoint.Transform(transform)
    urPoint.Transform(transform)

    blTrans = blPoint.ExportToWkt().split(" ")
    urTrans = urPoint.ExportToWkt().split(" ")

    origLat = round(float(blTrans[1][1:]))
    origLng = round(float(blTrans[2][0:-1]))
    refLat = round(float(urTrans[1][1:]))+30.  ## the 30 is hardcoded bc need to add bottom and right pixels and EO-1 has 30 meter pixels
    refLng = round(float(urTrans[2][0:-1]))-30.

    pixHeight = (origLat-refLat)/shape[1]
    pixWidth = (origLng-refLng)/shape[0]

    geoTrans = [origLat, pixWidth, 0, origLng, 0, pixHeight]
    
    return geoTrans

def getEPSG(metadata):
    projInfo = metadata['Projection']
    epsgLine = projInfo.split('\n')[-1].split('"')
    epsgNum = epsgLine[-2]
    return epsgNum

def getUTM(metadata):
    projInfo = metadata['Projection'].split('\n')[0]
    projSplit = projInfo.split(" ")
    return projSplit[-2][0:-2]
    
def getWGS(metadata):
    projInfo = metadata['Projection'].split('\n')[0]
    projSplit = projInfo.split(" ")
    return  int(projSplit[1])
