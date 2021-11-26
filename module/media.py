import cv2 as cv
import numpy as np


def img2npArray(imagePath, channel='all'):
    img = cv.imread(imagePath)
    if channel == 'all':
        result = img
    elif channel == 'B':
        result = img[:, 0].copy()
    elif channel == 'G':
        result = img[:, 1].copy()
    elif channel == 'R':
        result = img[:, 2].copy()
    return result


def res2Video(data, videoPath):
    row = data.shape[2]
    column = data.shape[3]

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(videoPath, fourcc, 20.0, (column, row))

    frame = np.empty((row, column, 3), dtype=np.uint8)
    for i in range(0, data.shape[1], 1):
        frame[:, :, 0] = data[0, i]
        frame[:, :, 1] = data[1, i]
        frame[:, :, 2] = data[2, i]
        out.write(frame)
    out.release()


def res2img(data, imgPath):
    row = data.shape[2]
    column = data.shape[3]
    frame = np.empty((row, column, 3), dtype=np.float32)
    for i in range(0, data.shape[1], 1):
        frame[:, :, 0] = data[0, i]
        frame[:, :, 1] = data[1, i]
        frame[:, :, 2] = data[2, i]
        cv.imwrite(imgPath+'%d.jpg' % i, frame)
