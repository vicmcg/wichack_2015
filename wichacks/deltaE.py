import cv2
import numpy
'''
title::
	deltaE.py

description::
	This method calculates the delta E of the images where delta E is
  from CIELAB space, and equals the distance between L*, a* and b*

attributes::
	rgb
		Source image to calculate cpsnr and cmse

return::
	delta_e
      The delta E mean value from the image. 
  delta_e_image    
      The delta E image array 

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

def deltaE( original, rgb , maxCount = 255):

  if original.shape != rgb.shape:
    err = 'Original and demosaicked images are not the same size.'
    raise RuntimeError( err )
  #fi

  original = original.astype(numpy.float32)
  rgb = rgb.astype(numpy.float32)

  original = original / maxCount
  rgb = rgb / maxCount

  # convert to lab
  lab = cv2.cvtColor( rgb, cv2.COLOR_BGR2LAB )
  lab_original = cv2.cvtColor( original, cv2.COLOR_BGR2LAB )

  l_difference = lab[ :, :, 0 ] - lab_original[ :, :, 0 ]
  a_difference = lab[ :, :, 1 ] - lab_original[ :, :, 1 ]
  b_difference = lab[ :, :, 2 ] - lab_original[ :, :, 2 ]

  delta_e_image = numpy.sqrt( l_difference**2 + a_difference**2 + b_difference**2 )
  delta_e = numpy.mean( delta_e_image )

  return delta_e, delta_e_image

#fed
