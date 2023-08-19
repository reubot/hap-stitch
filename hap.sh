#!/bin/bash
# generate tiffs from pdf

for var in "$@"
do  
  if [ "$var" ]; then	
  echo "$var"
    filetype=$(file "$var")
    echo $filetype
    mime=$(file --mime-type "$var")
    echo $mime

    echo pdfimages -all $var $var 
    pdfimages -all $var $var
    echo gdal_translate  $var-000.jpg $var-000.jpg.tiff -co COMPRESS=JPEG 
    gdal_translate  $var-000.jpg $var-000.jpg.tiff -co COMPRESS=JPEG 
  fi
done    
