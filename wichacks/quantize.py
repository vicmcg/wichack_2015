#Vic McGowen
#August 28 2014

import cv2
import wichacks
import numpy

'''
title::
   quantize

description::
   A method to quantize a given image either through uniform quantization
   or through improved grey-scale (igs) quantization. When doing Uniform 
   quantization, this method divides the entire image by the scale factor 
   found through dividing the macCount plus 1 over the float conversion of 
   the value of levels.
   
   IGS quantization part of the method loops through the image by rows, 
   columns and bands, adds the remainder to the current pixel from the 
   previous pixel if the value is not passed maxLevel, or does nothing 
   to the original value if it is above maxLevel. MaxLevel is found 
   through. The new pixel value is then divided by the scale divisor.

   For either type of quantization, once the quantizedImage is calculated,
   it is scaled by the display scale factor and returned. 

attributes:
   im
      Numpy ndArray of image to quantize
   levels
      Int defining how many levels to quantize to
   qtype
      A string defining type of quantization to do 
   maxCount
      Int of max bit depth
   displayLevels
      Int of max display bit depth
   disImage
      Numpy ndArray of type int of the final quantized image

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
def quantize(im, levels, qtype = 'uniform', maxCount = 255, displayLevels=None):
	
	# get columns, rows, colour bands and type from image
	numRows, numCol, numBands, dataType = wichacks.dimensions(im)
  
	numpix = numCol * numRows * numBands

	maxLevel = (maxCount + 1) - (2**(8 - levels))
	
	# scale for quantization
	divisor = ( maxCount + 1 ) / float( levels )

	# remainder used in igs
	remainder = 0
	
	quantizedImage = numpy.ndarray((2.2))
	
	 # error not working
	if(qtype != 'igs' and qtype != 'uniform' ):
		print 'Incorrect quantization type. Please try again'
    #fi

	# display scale to multiply final image by
	if displayLevels is None:
		displaymult  = 1
	else:
		displaymult = displayLevels / levels

	# igs quantization
	if( qtype is 'igs' ):

		# for coloured images
		if(numBands > 1):	 
			for co in range(0, numBands):
				for r in range(0, numRows):
					for c in range(0, numCol):
						# new pixel value at current location
						curr = im[r, c, co] + remainder	

						if ( curr >= maxLevel):
							curr = im[r,c,co]
						#fi 
						# save remainder
						remainder = curr % divisor

						im[r, c, co] = curr
					#rof
				#rof
			#rof
		#fi

		# 1D IGS
		else:
			for r in range(0, numRows):
				for c in range(0, numCol):	
					# new pixel value at current location        
					curr = im[r, c] + remainder					
					if ( curr > maxLevel):       		
						curr = im[r,c]						
					# save remainder        
					remainder = curr % divisor
 
					im[r,c] = curr
				#rof
			#rof
		#sele  
	#fi
	
	im = numpy.floor( im/ divisor )

	# final image is from the quantized image and the second scale
	# factor, displaymult
	disImage = im * displaymult
 
	return disImage.astype(dataType)

#fed

#Test Harness
if __name__ == '__main__':
	
	filename = 'game_images/lenna_color.tif'
	
	# reads in the file
	im = cv2.imread(filename, cv2.CV_LOAD_IMAGE_UNCHANGED)
	
	# makes window to display result
	cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename, im)

	numberLevels = 8
	quantizedImage = wichacks.quantize(im, numberLevels, qtype='uniform', displayLevels=256)
	
	cv2.namedWindow(filename + ' (Uniform Quantization)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (Uniform Quantization)', quantizedImage)
	
	numberLevels = 8
	quantizedImage = wichacks.quantize(im, numberLevels, qtype='igs', displayLevels=256)
	
	cv2.namedWindow(filename + ' (IGS Quantization)', cv2.WINDOW_AUTOSIZE)
	cv2.imshow(filename + ' (IGS Quantization)', quantizedImage)
	
	action = wichacks.flush()
#fi niam
