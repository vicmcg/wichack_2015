import wichacks
import math
import numpy

'''
title::
	cpsnr.py

description::
	This method calculates the colour-peak signal to noise ratio and
	the colour mean sum of the input image.

attributes::
	src
		Source image to calculate cpsnr and cmse

	rgb
		Demosaicked/reconstructed image to compare to source image

return::
	cpsnr
		Colour-peak siganl to noise ratio
	cmse
		Coloure mean squared error 

author::
	Vic McGowen

disclaimer::
  This source code is provided "as is" and without warranties as to 
  performance or merchantability. The author and/or distributors of 
  this source code may have made statements about this source code. 
  Any such statements do not constitute warranties and shall not be 
  relied on by the user in deciding whether to use this source code.
  
  This source code is provided without any express or implied warranties 
  whatsoever. Because of the diversity of conditions and hardware under 
  which this source code may be used, no warranty of fitness for a 
  particular purpose is offered. The user is advised to test the source 
  code thoroughly before relying on it. The user must assume the entire 
  risk of using the source code.
'''

def cpsnr( src, rgb, maxCount = 255 ):
	
	numRow, numCol, numBand, dataType = wichacks.dimensions( rgb )

	if src.shape != rgb.shape:
		err = 'Original and demosaicked images are not the same size.'
		raise RuntimeError( err )
	#fi

	multiplier = ( 1.0 / ( numBand * numCol * numRow ) )
	difference = numpy.sum( ( src - rgb ) ** 2 ) 
	cmse = multiplier * difference
	psnr = 10.0 * numpy.log10( ( maxCount ** 2) / cmse )

	return psnr, cmse
#fed

