import astropy
import numpy as np
import astropy.utils.data as AP_data
import astropy.io.fits as AP_fits
import matplotlib
import pprint

image = AP_data.download_file("http://data.astropy.org/tutorials/FITS-images/HorseHead.fits", cache=True)
image_data = AP_fits.getdata(image)

header = AP_fits.getheader(image)
pprint.pprint(header)