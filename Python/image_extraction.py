import PIL
import numpy as np
import matplotlib.pyplot as plt

# Nom de l'image
NAME = "ow.jpg"

SIZE = 42

image = plt.imread(NAME)
reconstruction = [[[0, 0, 0] for y in range(len(image[x]))] for x in range(len(image))]

def black_and_white(img):
    bw = []
    for l in range(len(img)):
        bw.append([])
        line = img[l]
        for pixel in line:
            color = [0, 0, 0]
            for i in range(3):
                if pixel[i] > 127 :
                    color[i] = 255
                else:
                    color[i] = 0
            bw[l].append(color)
    return bw

def extract(img):
    size = len(img)
    ratio = size / SIZE
    res = []
    image = [[img[x][y] for y in range(len(img[x]))] for x in range(len(img))]
    for i in range(180):
        radian = i / 180 * np.pi
        cos = np.cos(radian)
        sin = np.sin(radian)
        res.append([[0,0,0] for o in range(SIZE)])
        for j in range(SIZE // 2):
            k = j * ratio
            xPos1 = int(np.round(cos * k + size/2))
            yPos1 = int(np.round(sin * k + size/2))
            xPos2 = size - xPos1
            yPos2 = size - yPos1
            res[i][j+SIZE//2] = img[xPos1][yPos1]
            res[i][SIZE//2-j-1] = img[xPos2][yPos2]
            image[xPos1][yPos1] = [255,0,0]
            image[xPos2][yPos2] = [255,0,0]
    return res, image


# Pareil mais pour une ligne
def traceOne(extraction, support, pattern, angle):
    size = len(extraction)
    angle = int(np.floor(angle * (size / 180)))
    LEDS = extraction[angle]
    coords = pattern[angle]
    for i in range(len(coords)):
        x, y = coords[i]
        support[x][y] = LEDS[i]
    return support


def trace(extraction, support, pattern, angle):
    for i in range(angle):
        support = traceOne(extraction, support, pattern, i)
    return support


def eq_color(c1, c2):
    for i in range(len(c1)):
        if c1[i] != c2[i]:
            return False
    return True

def compress_color(c1, factor=20):
    color = []
    for c in c1:
        color.append(min(int(np.round(c/factor))*factor, 255))
    return color


def compress_img_color(img, factor=20):
    color = [[img[l][p] for p in range(len(img[l]))] for l in range(len(img))]
    for l in range(len(img)):
        for p in range(len(img[l])):
            color[l][p] = compress_color(img[l][p], factor)
    return color


def compress(img):
    compressed = []
    xSize = len(img)
    ySize = len(img[0])
    pixel = None
    count = 0
    compressed_pixel = 0
    for x in range(xSize):
        compressed.append([])
        for y in range(ySize):
            color = img[x][y]
            if y == 0:
                pixel = color
            if not eq_color(pixel, color):
                compressed[x].append((pixel, count))
                count = 0
                pixel = color
                compressed_pixel += count
            count += 1
        compressed[x].append((pixel, count))
        compressed_pixel += count
        count = 0
        pixel = None
    compression_rate = compressed_pixel / (xSize * ySize) * 100
    print("Compression rate : %s" % compression_rate)
    return compressed, compression_rate


def sampling(img, step):
    nSamples = 180 // step
    samples = []
    for i in range(nSamples):
        samples.append(img[i*step])
    return samples


# Sauvegarde l'image dans un .txt
def save(image):
    img = "const int EXTRACTION_SIZE = %s;\n" % len(image)
    img += "CRGB picture[EXTRACTION_SIZE][IMAGE_SIZE] = {"
    for l in range(len(image)):
        line = image[l]
        img += "{"
        for i in range(len(line)):
            r, g, b = line[i]
            img += "CRGB(%s, %s, %s)" % (r, g, b)
            if i != len(line)-1:
                img += ", "

        img += "}"
        if l != len(image)-1:
            img += ","
    img += "};\n"
    f = open("output.led", "w+")
    f.write(img)
    print("Saved")


# Image de base
plt.imshow(image)
plt.show()

# Image couleur compressée
image = compress_img_color(image, 15)
plt.imshow(image)
plt.show()

# Affiche l'image extraite
new_img, img = extract(image)

# Affiche l'image de base
plt.imshow(img)
plt.show()

# Affiche l'image de base
plt.imshow(new_img)
plt.show()

sampled = sampling(new_img, 15)
plt.imshow(sampled)
plt.show()
plt.show()

compressed, rating = compress(sampled)

save(sampled)

