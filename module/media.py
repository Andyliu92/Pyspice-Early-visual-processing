import cv2 as cv


def img2Voltage(imagePath, channel='all'):
    img = cv.imread(imagePath)
    if channel == 'all':
        result = img.copy()
    elif channel == 'B':
        result = img[:, 0].copy()
    elif channel == 'G':
        result = img[:, 1].copy()
    elif channel == 'R':
        result = img[:, 2].copy()
    return result
