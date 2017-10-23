# Usage
# python3 pointillize.py --image ./images/foto.png --radius 10 --cycles 20 --debug True
# python3 pointillize.py --image ./images/01.jpg --radius 10 --cycles 20 --debug True

import argparse
import cv2
import numpy as np
import random

################################################################################
##                          Functions                                         ##
################################################################################

def createRGBImage(height,width):
    empty_image = np.zeros((height,width,3), np.uint8)
    return empty_image

def createGrayImage(height,width):
    empty_image = np.zeros((height,width), np.uint8)
    return empty_image

def getPixelImage(image, row, col):
    return image[row][col]

def getChangedPixels(img):
    [rows,columns] = img.shape
    pxChangedPixels = []
    pyChangedPixels = []
    for i in range(rows):
        for j in range(columns):
            if(img[i][j] == 255):
                pxChangedPixels.append(i)
                pyChangedPixels.append(j)
    return (pxChangedPixels, pyChangedPixels)

def detectNewCircleColision(pxNewCircle, pyNewCircle, pxGlobal, pyGlobal):

    for i in range(len(pxNewCircle)):
        for circleNum in range(len(pxGlobal)):
            for x in range(len(pxGlobal[circleNum])):
                if(pxNewCircle[i] == pxGlobal[circleNum][x] and
                   pyNewCircle[i] == pyGlobal[circleNum][x]):
                   return True
    return False

def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

################################################################################
##                          Argument parser                                   ##
################################################################################
# construct the argument parser and parse the arguments
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()# for i in range(0,theta):
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-r", "--radius", required=True, help="Point's radius")
ap.add_argument("-c", "--cycles", required=True, help="Cycles")
ap.add_argument("-d", "--debug", required=True, help="Debug (True or False)")
args = vars(ap.parse_args())

# ------------          Source Image        ------------------------------------
sourcePath = args["image"]
radius = int(args["radius"])
cycles = int(args["cycles"])
if(args["debug"]=="True"):
    debug = True
else:
    debug = False

################################################################################
##                         Image Processing                                   ##
################################################################################
image = cv2.imread(sourcePath)

# Create new image
[rows,columns,color] = image.shape
if(debug):
    print("Rows = "+str(rows))
    print("Columns = "+str(columns))

# cv2.imwrite("inicio.png", image)

pointillizeImage = createRGBImage(rows,columns)
pointillizeImage = cv2.bitwise_not(pointillizeImage)
pointillizeGrayImage = createGrayImage(rows,columns)

pxAllChangedPixels = []
pyAllChangedPixels = []

result = detectNewCircleColision([0,3], [0,3], [[0,1],[3,4]], [[2,1],[3,4]])
if(debug):print(result)
for i in range(cycles):
    if(debug):print("Circle = " + str(i))
    addedCircleImage = createGrayImage(rows,columns)
    # New circle's location and color
    row = random.randint(0,rows - 1)
    col = random.randint(0,columns - 1)
    centerPixel = getPixelImage(image, row, col)
    color = (int(centerPixel[0]), int(centerPixel[1]), int(centerPixel[2]))

    # New circle's pixels
    cv2.circle(addedCircleImage, (col,row), radius, 255, -1)
    # pxChangedPixels, pyChangedPixels = getChangedPixels(addedCircleImage)

    xorImage = cv2.bitwise_xor(addedCircleImage, pointillizeGrayImage, mask = addedCircleImage)

    # Check if new Circle collides with another pixels
    if(is_similar(xorImage, addedCircleImage)):
        if(debug):print("Doesn't cause collision")
        # Add new circle to global array
        # pxAllChangedPixels.append(pxChangedPixels)
        # pyAllChangedPixels.append(pyChangedPixels)
        # Draw pixel in final image
        cv2.circle(pointillizeGrayImage, (col,row), radius, 255, -1)
        cv2.circle(pointillizeImage, (col,row), radius, color, -1)
    else:
        if(debug):print("Creates collision")

# print(pxAllChangedPixels)

cv2.imshow("Image", image)
cv2.imshow("Pointillize RGB", pointillizeImage)
cv2.imwrite("resultado.png", pointillizeImage)
cv2.waitKey(0)
