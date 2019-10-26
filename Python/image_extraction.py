import bresenham
import numpy as np
import matplotlib.pyplot as plt

# Nom de l'image
NAME = "60x.jpg"
# Taille de l'image
# La taille réelle de l'image devrait toujours être 1 pixel de plus (60 => 61x61)
SIZE = 60


image = plt.imread(NAME)
reconstruction = [[[0, 0, 0] for y in range(len(image[x]))] for x in range(len(image))]

# Quel pixel de l'image doit-on choisir pour tracer la ligne de (x0, y0) à (x1, y1)
def line(x0, y0, x1, y1):
    return list(bresenham.bresenham(x0, y0, x1, y1))


# Ligne de pixels pour chaque ligne de la matrice
def build_pattern_matrix(size):
    pattern_matrix = []
    for x in range(size):
        pattern_matrix.append(line(x, 0, size - x, size))

    for y in range(size):
        pattern_matrix.append(line(size, y, 0, size - y))

    return pattern_matrix


# Construit le tableau des couleurs de la bande LED pour chaque ligne
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
    return new_img, pattern_matrix


# Fonction de test pour tracer le dessin obtenu avec la rotation de la bande jusqu'à l'angle x
def trace(extraction, support, pattern, angle):
    for i in range(angle):
        support = traceOne(extraction, support, pattern, i)
    return support


# Pareil mais pour une ligne
def traceOne(extraction, support, pattern, angle):
    size = len(extraction)
    angle = int(np.floor(angle * (size / 180)))
    print(angle)
    LEDS = extraction[angle]
    coords = pattern[angle]
    for i in range(len(coords)):
        x, y = coords[i]
        support[x][y] = LEDS[i]
    return support


# Sauvegarde l'image dans un .txt
def save(image, step=10):
    img = "{"
    for l in range(len(image)):
        line = image[l]
        img += "{"
        for i in range(0, len(line), step):
            r, g, b = line[i]
            img += "CRGB(%s, %s, %s)" % (r, g, b)
            if i != len(line)-1:
                img += ", "

        img += "}"
        if l != len(image)-1:
            img += ","
    img += "}"
    f = open("output.led", "w+")
    f.write(img)


# Affiche l'image de base
plt.imshow(image)
plt.show()

# Affiche l'image extraite
new_img, pattern_matrix = extract(image, SIZE)
plt.imshow(new_img)
plt.show()

# Affiche la reconstruction de l'image à partir de l'image extraite jusqu'à l'angle x
reconstruction = trace(new_img, reconstruction, pattern_matrix, 180)
plt.imshow(reconstruction)
plt.show()

# Sauvegarde l'image
save(new_img)
