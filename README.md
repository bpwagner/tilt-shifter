# tilt-shifter
python program to create tilt-shifted photos

Run the python program tiltshifter.py

This program will take an image and then give it a tilt-shift effect, by taking an image, blurring it and 
alpha blending it with the original image.  It will also saturate the image if desired.

It is a command line program and here is the help instructions...

tiltshifter.py -i <inputfile> [-o <outputfile>] [-m <mask file>]
   other options
        -h help
        -p percent (10 is default)
        -y (vert center of image is default)
        -d display images
        -s saturate image
