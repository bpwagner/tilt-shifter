#!/usr/bin/python

import sys, getopt
import sys
import os
import numpy as np
import cv2

def printHelp():
    print 'tiltshifter.py -i <inputfile> [-o <outputfile>] [-m <mask file>]'
    print '   other options'
    print '        -h help'
    print '        -p percent (10 is default)'
    print '        -y (vert center of image is default)'
    print '        -d display images'
    print '        -s saturate image'
    print
    print '  by Brian Wagner for OMSCS CS 6475, Spring 2016'
    print '     bpwagner@gatech.edu'

def displayImages(image, mask, image_out):
        scale = image.shape[1]/1024
        newx,newy = image.shape[1]/scale ,image.shape[0]/scale #new size (w,h)
        newimage = cv2.resize(image,(newx,newy))
        cv2.imshow('input image', newimage)
        newmask = cv2.resize(mask,(newx,newy))
        cv2.imshow('mask image', newmask)
        newimage_out = cv2.resize(image_out,(newx,newy))
        cv2.imshow('output image', newimage_out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def makeMask(img, maskY, percent):

    mask = np.copy(img)
    percentPixels = int(mask.shape[0] * (percent/100))
    borderPixels = percentPixels / 4
    startY = maskY - percentPixels / 2
    endY = maskY + percentPixels/2
    if startY<0:
        startY =0
    if endY > mask.shape[0]:
        endY = mask.shape[0]

    for col in range(mask.shape[1]):
        for row in range(mask.shape[0]):
            if row < startY - borderPixels *2 :
                mask[row,col] = 0
            elif row < startY - borderPixels:
                mask[row,col] = 100
            elif row < startY:
                mask[row,col] = 200
            elif row < endY:
                mask[row,col] = 255
            elif row < endY + borderPixels:
                mask[row,col] = 200
            elif row < endY + borderPixels * 2:
                mask[row,col] = 100
            else:
                mask[row,col] = 0

    #blur the mask a bit
    mask = cv2.GaussianBlur(mask,(25,25),5)
    return mask

def tiltShift(image, mask):
    image_out = np.copy(image)

    blurred_image = cv2.GaussianBlur(image,(25,25),4)

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            alpha = mask[row,col] / 255.0
            pixel = image[row,col] * alpha + blurred_image[row,col] * (1-alpha)
            #print row, col,  alpha, pixel
            image_out[row,col] = pixel


    # cv2.imshow('output image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image_out


def saturateIimage(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    for row in range(hsv_image.shape[0]):
        for col in range(hsv_image.shape[1]):

            hsv_image[row,col][1] = hsv_image[row,col][1] + 20
            if hsv_image[row,col][1] > 255:
                hsv_image[row,col][1] = 255

            hsv_image[row,col][2] = hsv_image[row,col][2] + 10
            if hsv_image[row,col][2] > 255:
                hsv_image[row,col][2] = 255


    image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return image



def main(argv):
    inputfile = ''
    outputfile = ''
    maskfile = ''
    display = False
    saturate = False
    saveFile = False
    percent = 10.0
    maskX = -1
    maskY = -1
    try:
        opts, args = getopt.getopt(argv,"hi:o:m:dp:y:s")
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputfile = arg
            saveFile = True
        elif opt == '-m':
            maskfile = arg
        elif opt == '-p':
            percent = float(arg)
        elif opt == '-y':
            maskY =int(arg)
        elif opt == '-d':
            display = True
        elif opt == '-s':
            saturate = True

    print 'Reading input file: ', inputfile
    #check for valid input file
    img = cv2.imread(inputfile)

    if maskfile != '':
        print 'Reading the maskfile.'
        mask = cv2.imread(maskfile)
    else:
        print 'Generating the mask.'
        #make mask
        if maskX == -1:
            maskX = img.shape[1]/2
        if maskY == -1:
            maskY = img.shape[0]/2
        mask = makeMask(img, maskY, percent)

    print 'Running the tiltshifter.'
    #run tiltshifter
    img_out = tiltShift(img,mask)

    #run saturizer
    if saturate:
        print 'Running the saturator.'
        img_out = saturateIimage(img_out)

    #display if needed
    if display:
        print 'Displaying the images.'
        displayImages(img, mask, img_out)

    if saveFile:
        print 'Saving output file: ', outputfile
        cv2.imwrite(outputfile,img_out)

    print 'All done.'

if __name__ == "__main__":
   main(sys.argv[1:])