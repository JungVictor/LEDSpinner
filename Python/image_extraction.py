import PIL
import numpy as np
import matplotlib.pyplot as plt

IMAGE_DIR = "images/"
OUTPUT_DIR = "output/"
LINEAR = 0
POW2 = 1
CONSTANT = 2
############################################
# CONFIGURATION
############################################
# Nom du fichier de sauvegarde
FILE_NAME = "sonic"
# Nom des images
NAME = ["sonic-gif1.jpg", "sonic-gif2.jpg", "sonic-gif3.jpg", "sonic-gif4.jpg",
        "sonic-gif5.jpg", "sonic-gif6.jpg"]

# On compresse les couleurs ?
COMPRESS_COLOR = False
# Si oui, de combien ?
COLOR_APPROX_FACTOR = 50
# Combien de ligne d'angle on garde
SAMPLING = [45, 90]  # Traditionnel
COMPRESSION_SAMPLING = [45, 90]  # Nouveau

# Méthode de compression automatique (pour l'instant pas ouf)
COMPRESSED_INDEX_METHOD = LINEAR

SHOW_IMAGE = True
SHOW_COMPRESSED_IMAGE = False
SHOW_SAMPLING_POINTS = False
SHOW_EXTRACTED_IMAGE = False
SHOW_SAMPLED_IMAGE = False
SHOW_RECONSTRUCTED_IMAGE = True

# Taille de la bande de LED
SIZE = 42
############################################

images = [plt.imread(IMAGE_DIR + n) for n in NAME]
reconstruction = [[[0, 0, 0] for y in range(len(images[0][x]))] for x in range(len(images))]


# Prend en entrée un tableau de taille d'échantillon pour chaque LED,
# et renvoit un tableau qui correspond à la position du premier index
# [2, 4, 8, 16, 32] -> [0, 2, 6, 14, 30, 62]
def build_positions(sizes):
    sizes = symmetry(sizes)
    index_position = [0]
    for i in range(1, len(sizes) + 1):
        index_position.append(index_position[i - 1] + sizes[i - 1])
    return sizes, index_position


def symmetry(sizes, even=True):
    sym = []
    for i in range(len(sizes)):
        sym.append(sizes[-(i + 1)])
    start = 1
    if even:
        start = 0
    for i in range(start, len(sizes)):
        sym.append(sizes[i])
    return sym


##################################
# FONCTIONS DE DISTRIBUTIONS (?)
# A REFAIRE /!\ (manuel pour 42 ?)
##################################
# CONSTANTE
def constant(num_led, max_size):
    mid = int(np.ceil(num_led / 2))
    index_size = [max_size for i in range(mid)]
    return build_positions(index_size)


# LINEAIRE
def linear(num_led, max_size):
    mid = int(np.ceil(num_led / 2))
    index_size = [max(0, round(i * (max_size / mid) + 1)) for i in range(mid)]
    return build_positions(index_size)


# PUISSANCE 2
def pow2(num_led, max_size):
    mid = int(np.ceil(num_led / 2))
    index_size = [min(max_size, int(round(np.log2((i + 1) * 8) * 4))) for i in range(mid)]
    return build_positions(index_size)


# "Factory" pour générer en fonction du paramètre "type"
def size_and_pos(type, size, led=SIZE):
    if type == LINEAR:
        return linear(led, size)
    if type == POW2:
        return pow2(led, size)
    return constant(led, size)


#################################


# Modifie les couleurs de l'image pour que les couleurs soient sur 1 bit (8 couleurs)
def bit(img):
    bw = []
    for l in range(len(img)):
        bw.append([])
        line = img[l]
        for pixel in line:
            color = [0, 0, 0]
            for i in range(3):
                if pixel[i] > 127:
                    color[i] = 255
                else:
                    color[i] = 0
            bw[l].append(color)
    return bw


# Modifie les couleurs de l'image pour qu'elle soit en noir et blanc (pas de nuance)
def black_and_white(img):
    bw = []
    for l in range(len(img)):
        bw.append([])
        line = img[l]
        for pixel in line:
            color = [0, 0, 0]
            c = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
            if c > 381:
                color = [255, 255, 255]
            bw[l].append(color)
    return bw


def mean(image, xPos, yPos, s):
    if s == 0:
        return image[xPos][yPos]
    color = [0, 0, 0]
    cpt = 0
    for x in range(xPos-s, xPos+s):
        for y in range(yPos-s, yPos+s):
            if (x >= 0 and y >= 0) and (x < len(image) and y < len(image[0])):
                color[0] += image[x][y][0]
                color[1] += image[x][y][1]
                color[2] += image[x][y][2]
            cpt += 1
    color[0] /= cpt
    color[1] /= cpt
    color[2] /= cpt
    return color


# Extrait les pixels de l'image d'origine
# Renvoit une image polaire + l'image d'origine avec les pixels échantillonés en rouge
def extract(img, LED=SIZE):
    size = min(len(img), len(img[0]))
    ratio = size / LED
    res = []
    image = [[img[x][y] for y in range(len(img[x]))] for x in range(len(img))]
    HALF = LED // 2
    for i in range(180):
        radian = i / 180 * np.pi
        cos = np.cos(radian)
        sin = np.sin(radian)
        res.append([[0, 0, 0] for o in range(LED)])
        for j in range(HALF):
            k = j * ratio
            xPos1 = int(np.round(cos * k + size / 2))
            yPos1 = int(np.round(sin * k + size / 2))
            xPos2 = size - xPos1
            yPos2 = size - yPos1
            res[i][j + HALF] = mean(img, xPos1, yPos1, 0)
            res[i][HALF - j - 1] = mean(img, xPos2, yPos2, 0)
            image[xPos1][yPos1] = [255, 0, 0]
            image[xPos2][yPos2] = [255, 0, 0]
    return res, image


# Compare deux couleurs et renvoit True si elles sont égales, False sinon.
def eq_color(c1, c2):
    for i in range(len(c1)):
        if c1[i] != c2[i]:
            return False
    return True


# On compresse les couleurs selon un facteur.
# Si le facteur est 1 -> identité
# Si le facteur est 20 : 0 -> 0, 15 -> 20 etc...
def compress_color(c1, factor=20):
    color = []
    for c in c1:
        color.append(min(int(np.round(c / factor)) * factor, 255))
    return color


# On compresse toutes les couleurs de l'image selon un facteur
def compress_img_color(img, factor=20):
    color = [[img[l][p] for p in range(len(img[l]))] for l in range(len(img))]
    for l in range(len(img)):
        for p in range(len(img[l])):
            color[l][p] = compress_color(img[l][p], factor)
    return color


# NOUVELLE METHODE !!!
# On compresse l'image en fonction d'un nombre d'échantillon pour chaque LED
def compress(img, type=LINEAR, SAMPLING_SIZE=45, size=SIZE):
    compression_size, positions = size_and_pos(type, SAMPLING_SIZE, size)
    compressed = []
    for i in range(size):
        s = compression_size[i]
        for j in range(s):
            j = j % s
            index = round(179 * j / s)
            compressed.append(img[index][i])
    #print("Compression : %s" % (len(compressed) / (size * 45)))
    return compressed, positions


# ANCIENNE METHODE
# On compresse l'image en échantillonant de manière constante
def sampling(img, step):
    nSamples = 180 // step
    samples = []
    for i in range(step):
        samples.append(img[i * nSamples])
    return samples


# Retourne la taille de l'échantillon pour la LED index
def getSize(positions, index):
    return positions[index + 1] - positions[index]


# Retourne le pixel correspondant à l'angle à la LED index.
def getPixel(angle, index, img, positions):
    return img[round(angle * (getSize(positions, index) - 1)) + positions[index]]


# NOUVELLE METHODE !!
# Reconstruit l'image à partir de l'image compressée (vérification)
def reconstruct_img(compressed, positions, size=SIZE, c=(0,0,0)):
    reconstructed = [[[c[0], c[1], c[2]] for i in range(size)] for j in range(size)]
    for i in range(180, 0, -1):
        radian = i / 180 * np.pi
        cos = np.cos(radian)
        sin = np.sin(radian)
        half = size // 2
        for led in range(half):
            xPos1 = int(np.round(cos * led + size / 2))
            yPos1 = int(np.round(sin * led + size / 2))
            xPos2 = size - xPos1
            yPos2 = size - yPos1
            reconstructed[xPos1][yPos1] = getPixel(i / 180, led + half, compressed, positions)
            reconstructed[xPos2][yPos2] = getPixel(i / 180, half - led - 1, compressed, positions)
    return reconstructed


# ANCIENNE METHODE !!
# Reconstruit l'image à partir de l'image compressée (vérification)
def reconstruct(img):
    reconstructed = [[[0, 0, 0] for i in range(SIZE)] for j in range(SIZE)]
    size = SIZE
    for i in range(180, 0, -1):
        radian = i / 180 * np.pi
        cos = np.cos(radian)
        sin = np.sin(radian)
        index = int(np.round(i * (len(img) - 1) / 180))
        for j in range(SIZE // 2):
            k = j
            xPos1 = int(np.round(cos * k + size / 2))
            yPos1 = int(np.round(sin * k + size / 2))
            xPos2 = size - xPos1
            yPos2 = size - yPos1
            reconstructed[xPos1][yPos1] = img[index][j + SIZE // 2]
            reconstructed[xPos2][yPos2] = img[index][SIZE // 2 - j - 1]
    return reconstructed


# Sauvegarde l'image dans un .led
def save(txt):
    filename = OUTPUT_DIR + FILE_NAME + "-%s-%s.led" % (len(NAME), SAMPLING[-1])
    f = open(filename, "w+")
    f.write(txt)
    print("Saved as %s" % filename)


# NOUVELLE METHODE !!
# Génère le code de l'image
def generate(compression, positions):
    return "CRGB COLORS[] = %s;\nint POSITIONS[] = %s;\n" % (compression, positions)


# ANCIENNE METHODE !!
# Génère le code de l'image
def generateCode(image):
    dico = {}
    for l in range(len(image)):
        line = image[l]
        for p in range(len(line)):
            r, g, b = line[p]
            pixel = "CRGB(%s, %s, %s)" % (r, g, b)
            if not pixel in dico:
                dico[pixel] = []
            dico[pixel].append((l, p))

    code = ""
    TAB = "\t"
    if len(NAME) > 1:
        TAB += TAB
    colors = sorted(dico, key=lambda k: len(dico[k]), reverse=False)
    for c in range(len(colors) - 1):
        color = colors[c]
        position = dico[color]
        if c == 0:
            condition = TAB + "if ("
        else:
            condition = TAB + "else if ("
        for p in range(len(position) - 1):
            condition += "(angle == %s && index == %s) || " % position[p]
        condition += "(angle == %s && index == %s)" % position[-1]
        condition += ") return " + color + ";\n"
        code += condition
    code += TAB + "else return %s;" % colors[-1]
    return code


images = [bit(image) for image in images]
CODE = "const int EXTRACTION_SIZE = %s;\nconst int N_IMAGE = %s;\nCRGB getColor(int angle, int index){\n" % (SAMPLING[-1], len(NAME))
cpt = 0


def compute(image, led_num=42, compress_color=False, color_approx_factor=50, compressed_index_method=LINEAR, sampling_size=90, c=(0,0,0), bit3=True):
    new_img, img = extract(image, led_num)
    if bit3:
        new_img = bit(new_img)
    elif compress_color:
        new_img = compress_img_color(new_img, color_approx_factor)
    compressed, positions = compress(new_img, compressed_index_method, sampling_size, led_num)
    reconstruction = reconstruct_img(compressed, positions, led_num, c)

    return new_img, compressed, reconstruction, positions


if __name__ == "__main__":
    for image in images:
        # Image de base
        if SHOW_IMAGE:
            plt.imshow(image)
            plt.title("Image de base")
            plt.show()

        image = compress_img_color(image, COLOR_APPROX_FACTOR)

        # Image couleurs compressées
        if SHOW_COMPRESSED_IMAGE:
            plt.imshow(image)
            plt.title("Image compressée")
            plt.show()

        # Calcul l'image extraite
        new_img, img = extract(image)

        # Affiche l'image de base
        if SHOW_SAMPLING_POINTS:
            plt.imshow(img)
            plt.title("Échantillonnage")
            plt.show()

        # Affiche l'image extraite
        if SHOW_EXTRACTED_IMAGE:
            plt.imshow(new_img)
            plt.title("Image extraite")
            plt.show()

        sampled = []
        for s in SAMPLING:
            sampled.append(sampling(new_img, s))
        if SHOW_SAMPLED_IMAGE:
            for i in range(len(sampled)):
                plt.imshow(sampled[i])
                plt.title("Image extraite échantillonnée (%s)" % SAMPLING[i])
                plt.show()

        if SHOW_RECONSTRUCTED_IMAGE:
            for i in range(len(sampled)):
                compressed, positions = compress(new_img, COMPRESSED_INDEX_METHOD, COMPRESSION_SAMPLING[i])
                reconstruction = reconstruct_img(compressed, positions)
                plt.imshow(reconstruction)
                plt.title("Image reconstruite (%s) NEW" % SAMPLING[i])
                plt.show()

                reconstruction = reconstruct(sampled[i])
                plt.imshow(reconstruction)
                plt.title("Image reconstruite (%s) OLD" % SAMPLING[i])
                plt.show()

        sampled = sampled[-1]

        if cpt == len(images) - 1:
            if len(NAME) > 1:
                CODE += "\telse {\n%s\n\t}\n" % generateCode(sampled)
            else:
                CODE += "%s\n" % generateCode(sampled)
        else:
            CODE += "\tif(IMAGE == %s) {\n%s\n\t}\n" % (cpt, generateCode(sampled))
        cpt += 1

    CODE += "}"

    save(CODE)
