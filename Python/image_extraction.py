import bresenham
import numpy as np
import matplotlib.pyplot as plt

NAME = "line.jpg"
SIZE = 30
ANGLE = 360

image = plt.imread(NAME)


def line(x0, y0, x1, y1):
    return list(bresenham.bresenham(x0, y0, x1, y1))


def build_pattern_matrix(size):
    pattern_matrix = []
    diag = int(np.floor(np.sqrt(2)*size)) // 2
    hSize = size // 2
    for degree in range(0, ANGLE):
        radian = degree / 180 * np.pi
        cosDiag = int(np.round(np.cos(radian)*diag))
        sinDiag = int(np.round(np.sin(radian)*diag))

        if cosDiag < 0: xDest = 0
        else: xDest = min(int(np.round(cosDiag)), hSize) + hSize
        if sinDiag < 0: yDest = 0
        else: yDest = min(int(np.round(sinDiag)), hSize) + hSize

        xSource = size - xDest
        ySource = size - yDest
        pattern_matrix.append(line(xSource, ySource, xDest, yDest))
    return pattern_matrix


def extract(img, size):
    pattern_matrix = build_pattern_matrix(size)
    new_img = []
    for i in range(len(pattern_matrix)):
        deg = pattern_matrix[i]
        line = []
        for j in range(len(deg)):
            x, y = deg[j]
            line.append(img[x][y])
        new_img.append(line)
    return new_img


new_img = extract(image, SIZE)
plt.imshow(new_img)
plt.show()


def save(image, step=10):
    img = "{"
    for l in range(len(image)):
        line = image[l]
        img += "{"
        for i in range(len(line), step=step):
            r, g, b = line[i]
            img += "CRGB(%s, %s, %s)" % (r, g, b)
            if i != len(line)-1:
                img += ", "

        img += "}"
        if l != len(image)-1:
            img += ","
    img += "}"
    f = open("output.txt", "w+")
    f.write(img)


save(new_img)

