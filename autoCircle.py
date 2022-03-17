import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
imagePath = "yourImagesPath/"
for filename in os.listdir(imagePath):
    img = cv2.imread(imagePath+filename)
    print(filename)
    # img = img[150:450, 150:450]
    blur = cv2.medianBlur(img, 21)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    thresh = 20
    imBW = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
    # plt.imshow(imBW)
    # plt.show()
    circles = cv2.HoughCircles(
        imBW, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # circles = cv2.HoughCircles(imBW, cv2.HOUGH_GRADIENT, 1, 20, param1=30, param2=90, minRadius=0, maxRadius=225)
    list_circles = []
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            topX = i[0] - i[2]
            topY = i[1] - i[2]
            bottomX = i[0] + i[2]
            bottomY = i[1] + i[2]
            if topX < 0 or topY < 0 or bottomX > img.shape[0] or bottomY > img.shape[1]:
                continue
            else:
                # Center = i[0], i[1]
                leftSide = (bottomX, int((topY+bottomY)/2))
                topSide = (int((topX+bottomX)/2), topY)
                rightSide = (topX, int((topY+bottomY)/2))
                bottomSide = (int((topX+bottomX)/2), bottomY)
                if leftSide[0] < 0 or leftSide[1] < 0 or rightSide[0] > img.shape[0] or rightSide[1] > img.shape[1] or topSide[0] < 0 or topSide[1] < 0 or bottomSide[0] > img.shape[0] or bottomSide[1] > img.shape[1]:
                    continue
                else:
                    # cv2.rectangle(img, (i[0] - i[2], i[1] - i[2]),
                    #               (i[0] + i[2], i[1] + i[2]), (255, 0, 0), 1)
                    for side in [leftSide, topSide, rightSide, bottomSide]:
                        cv2.circle(img, side, 2, (0, 255, 0), -1)
                    print("radius:", i[2])
                    print("upperCorner:", topX, topY)
                    print("lowerCorner:", bottomX, bottomY)
    plt.imshow(img)
    plt.show()
