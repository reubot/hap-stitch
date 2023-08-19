#https://stackoverflow.com/questions/55681995/how-to-georeference-an-unreferenced-aerial-image-using-ground-control-points-in

import shutil
from osgeo import gdal, osr
import json

photoid = 5088
year=1951
run=2
orig_fn = '../www.actmapi.act.gov.au/hap/'+str(year)+'/'+str(run)+'/'+ str(photoid) +'.pdf-000.jpg.tiff'
output_fn = orig_fn+'.geotiff'
jfile = open( "1950sfeatures.json" , "r" )
j1950s = json.load(jfile)
j1950sfeatures = j1950s["features"]
# print(json.dumps(j1950s))
filtered_list = [x for x in j1950sfeatures if  (x['attributes']["PHOTO"] == photoid and x['attributes']["CAPTURE"] == year and x['attributes']["RUN"] == run)]
print(filtered_list)
# Create a copy of the original file and save it as the output filename:
shutil.copy(orig_fn, output_fn)
# Open the output file for writing for writing:
ds = gdal.Open(output_fn, gdal.GA_Update)
xres = ds.RasterXSize
yres = ds.RasterYSize
rings=filtered_list[0]["geometry"]["rings"][0]
print(xres, yres,rings)
# Set spatial reference:
sr = osr.SpatialReference()
sr.ImportFromEPSG(7855) #2193 refers to the NZTM2000, but can use any desired projection

# Enter the GCPs
#   Format: [map x-coordinate(longitude)], [map y-coordinate (latitude)], [elevation],
#   [image column index(x)], [image row index (y)]
gcps = [
gdal.GCP(rings[0][0], rings[0][1], 0, 0, 0),
gdal.GCP(rings[1][0], rings[1][1], 0, 0, yres),
gdal.GCP(rings[2][0], rings[2][1], 0, xres, yres),
gdal.GCP(rings[3][0], rings[3][1], 0, xres, 0)
]

# Apply the GCPs to the open output file:
ds.SetGCPs(gcps, sr.ExportToWkt())

# Close the output file in order to be able to work with it in other programs:
ds = None
 
