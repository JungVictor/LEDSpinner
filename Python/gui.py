# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from image_extraction import compute
import numpy

IMAGES = []
GENERATED = []

frameCnf = {"bg": "#3c3f41"}
font = ("Verdana", 10, "bold")

window = Tk()
window.title("LEDSpinner Image Converter")
window.geometry("560x730")
window.resizable(False, False)
window.config(cnf=frameCnf)
icon = PhotoImage(file='LEDSpinner.png')
closebutton = PhotoImage(file='close.png')
window.tk.call('wm', 'iconphoto', window._w, icon)

IMAGE_PREVIEW_SIZE = 120
IMAGE_PREVIEW_MARGIN = 4
IMAGE_PREVIEW_MAX_PER_LINE = 4


def remove(id):
    del IMAGES[id]
    draw_all_images()
    cImages.config(cursor="")


def draw_all_images():
    cpt = 0
    offset = IMAGE_PREVIEW_SIZE + IMAGE_PREVIEW_MARGIN
    cImages.delete("all")
    for image in IMAGES:
        x, y = (cpt % IMAGE_PREVIEW_MAX_PER_LINE, cpt // IMAGE_PREVIEW_MAX_PER_LINE)
        img = image.resize((IMAGE_PREVIEW_SIZE, IMAGE_PREVIEW_SIZE))
        draw_image(x*offset, y*offset, ImageTk.PhotoImage(img), cpt)
        cpt += 1

    cImages.configure(yscrollcommand=fImagesScrollBar.set, scrollregion=cImages.bbox("all"))


def draw_all_generated_images():
    cpt = 0
    offset = IMAGE_PREVIEW_SIZE + IMAGE_PREVIEW_MARGIN
    for image in GENERATED:
        x, y = (cpt % IMAGE_PREVIEW_MAX_PER_LINE, cpt // IMAGE_PREVIEW_MAX_PER_LINE)
        img = image.resize((IMAGE_PREVIEW_SIZE, IMAGE_PREVIEW_SIZE))
        draw_generated_image(x*offset, y*offset, ImageTk.PhotoImage(img), cpt)
        cpt += 1

    cImagesGenerated.configure(yscrollcommand=fImagesScrollBarGenerated.set, scrollregion=cImagesGenerated.bbox("all"))


def draw_image(x, y, image, name):
    cImages.create_image(x, y, image=image, anchor=NW)
    close = cImages.create_image(x+IMAGE_PREVIEW_SIZE, y, image=closebutton, anchor=NE)
    cImages.tag_bind(close, '<1>', lambda rem: remove(name))
    cImages.tag_bind(close, '<Enter>', lambda x: cImages.config(cursor="hand2"))
    cImages.tag_bind(close, '<Leave>', lambda x: cImages.config(cursor=""))
    cImages.images[name] = image
    cImages.close = closebutton
    cImages.update()


def draw_generated_image(x, y, image, name):
    cImagesGenerated.create_image(x, y, image=image, anchor=NW)
    cImagesGenerated.images[name] = image
    cImagesGenerated.update()


def open_image():
    filename = tkinter.filedialog.askopenfilenames(
        title="Choose an image",
        filetypes=[('JPG files', '.jpg'), ('GIF files', '.gif'), ('all files', '.*')]
    )
    if filename is not "":
        files = window.tk.splitlist(filename)
        for file in files:
            if file[-3:] == "gif":
                gif = Image.open(file)
                cpt = 1
                try:
                    while True:
                        IMAGES.append(gif.copy().convert('RGB'))
                        gif.seek(cpt)
                        cpt += 1
                except EOFError:
                    pass
            else:
                IMAGES.append(Image.open(file))
        draw_all_images()


def clear():
    IMAGES.clear()
    cImages.delete("all")
    draw_all_images()


def clear_generated():
    GENERATED.clear()
    cImagesGenerated.delete("all")



cnfButtons = {
    "relief": "flat",
    "padx": 10, "pady": 10,
    "bd": 0,
    "activebackground": "#3498db", "bg": "#85c1e9",
    "font": font,
    "cursor": "hand2"
}

cnfEntries = {
    "bg": "#5e6062",
    "relief": "flat",
    "width": 3,
    "fg": "#bbbbbb",
    "bd": 2,
    "justify": "center"
}
###############
# MENU TOP
###############
# Buttons
MENU_TOP = Frame(window, cnf=frameCnf, bg="#2b2b2b")
bOpenImage = Button(MENU_TOP, text="Add image", command=open_image, cnf=cnfButtons)
bClearAll = Button(MENU_TOP, text="Clear", command=clear, cnf=cnfButtons, bg="#f5b7b1", activebackground="#e74c3c")


bClearAll.pack(side=RIGHT, padx=10, pady=8)
bOpenImage.pack(side=RIGHT, padx=10, pady=8)
###############

###############
# IMAGES FRAME
###############
IMAGE_PREVIEW = Frame(window, cnf=frameCnf)
# Main Frame
fImages = Frame(IMAGE_PREVIEW, bg="black")

# Canvas and Scrollbar
fImagesWidth = (IMAGE_PREVIEW_SIZE+IMAGE_PREVIEW_MARGIN)*IMAGE_PREVIEW_MAX_PER_LINE
fImagesHeight = (IMAGE_PREVIEW_SIZE+IMAGE_PREVIEW_MARGIN)*2

cImages = Canvas(fImages, width=fImagesWidth, height=fImagesHeight)
fImagesScrollBar = Scrollbar(fImages, orient=VERTICAL)
fImagesScrollBar.configure(command=cImages.yview)
cImages.configure(yscrollcommand=fImagesScrollBar.set, scrollregion=cImages.bbox("all"))

cImages.images = {}


fImages.pack()
fImagesScrollBar.pack(side=RIGHT, fill=Y)
cImages.pack(side=LEFT, fill=X)
###############

###############
# IMAGES GENERATED
###############
IMAGE_GENERATED = Frame(window, cnf=frameCnf)
# Main Frame
fImagesGenerated = Frame(IMAGE_GENERATED, bg="black")

# Canvas and Scrollbar
cImagesGenerated = Canvas(fImagesGenerated, width=fImagesWidth, height=fImagesHeight, bg="#282828")
fImagesScrollBarGenerated = Scrollbar(fImagesGenerated, orient=VERTICAL)
fImagesScrollBarGenerated.configure(command=cImagesGenerated.yview)
cImagesGenerated.configure(yscrollcommand=fImagesScrollBarGenerated.set, scrollregion=cImagesGenerated.bbox("all"))

cImagesGenerated.images = {}


fImagesGenerated.pack()
fImagesScrollBarGenerated.pack(side=RIGHT, fill=Y)
cImagesGenerated.pack(side=LEFT, fill=X)
###############

###############
# INPUT
###############
INPUT = Frame(window, cnf=frameCnf, bg="#3c3f41")
LINE1 = Frame(INPUT, cnf=frameCnf)
LINE2 = Frame(INPUT, cnf=frameCnf)
LINE3 = Frame(INPUT, cnf=frameCnf)

LED_INPUT = Frame(LINE1, cnf=frameCnf)
FPS_INPUT = Frame(LINE2, cnf=frameCnf)
SAMPLING_INPUT = Frame(LINE1, cnf=frameCnf)
COLOR_INPUT = Frame(LINE2, cnf=frameCnf)
BIT3_INPUT = Frame(LINE3, cnf=frameCnf)

NUM_LED = IntVar()
NUM_FPS = IntVar()
NUM_SAMPLING = IntVar()
NUM_COLOR_COMPRESS = IntVar()
BOOL_BIT3 = IntVar()

NUM_LED.set(42)
NUM_SAMPLING.set(90)
NUM_COLOR_COMPRESS.set(0)
BOOL_BIT3.set(1)

text_color = "#cb602d"

LED_num_text = Label(LED_INPUT, text="Number of LED : ", cnf=frameCnf, fg=text_color, font=font)
LED_num_entry = Entry(LED_INPUT, text=NUM_LED, cnf=cnfEntries)
LED_num_text.pack(side=LEFT)
LED_num_entry.pack(side=LEFT)

FPS_num_text = Label(FPS_INPUT, text="FPS : ", cnf=frameCnf, fg=text_color, font=font)
FPS_num_entry = Entry(FPS_INPUT, text=NUM_FPS, cnf=cnfEntries)
FPS_num_text.pack(side=LEFT)
FPS_num_entry.pack(side=LEFT)

SAMPLING_num_text = Label(SAMPLING_INPUT, text="SAMPLING : ", cnf=frameCnf, fg=text_color, font=font)
SAMPLING_num_entry = Entry(SAMPLING_INPUT, text=NUM_SAMPLING, cnf=cnfEntries)
SAMPLING_num_text.pack(side=LEFT)
SAMPLING_num_entry.pack(side=LEFT)

COLOR_num_text = Label(COLOR_INPUT, text="COLOR COMPRESSION FACTOR : ", cnf=frameCnf, fg=text_color, font=font)
COLOR_num_entry = Entry(COLOR_INPUT, text=NUM_COLOR_COMPRESS, cnf=cnfEntries)
COLOR_num_text.pack(side=LEFT)
COLOR_num_entry.pack(side=LEFT)

BIT3_text = Checkbutton(BIT3_INPUT, text="3 BIT COLORS", cnf=frameCnf, fg=text_color, font=font, variable=BOOL_BIT3)
BIT3_text.pack(side=LEFT)

LINE1.pack(side=TOP, fill=X, padx=40)
LED_INPUT.pack(side=LEFT)
SAMPLING_INPUT.pack(side=RIGHT)

LINE3.pack(side=BOTTOM, fill=X, padx=40)
BIT3_INPUT.pack(side=RIGHT)

LINE2.pack(side=BOTTOM, fill=X, padx=40)
FPS_INPUT.pack(side=LEFT)
COLOR_INPUT.pack(side=RIGHT)
###############
progress = ttk.Progressbar(window, orient=HORIZONTAL, mode="determinate", maximum=100)


def get_num_led():
    return int(NUM_LED.get())


def get_num_fps():
    return int(NUM_FPS.get())


def get_num_sampling():
    return int(NUM_SAMPLING.get())


def get_num_color_compression():
    c = int(NUM_COLOR_COMPRESS.get())
    if c <= 0:
        return 1
    return c


def is_3bit():
    return int(BOOL_BIT3.get()) > 0


def next_animation(canvas):
    canvas.delete("all")
    canvas.cpt = (canvas.cpt + 1) % len(canvas.images)
    canvas.create_image(0, 0, image=canvas.images[canvas.cpt], anchor=NW)
    canvas.after(canvas.delay, next_animation, canvas)


def play_animation():
    if len(GENERATED) <= 0:
        return
    size = 400
    animation = Toplevel()
    animation.tk.call('wm', 'iconphoto', animation._w, icon)
    animation.geometry("%sx%s" % (size, size))
    animation.resizable(False, False)
    animation.config(takefocus=True)
    animation.lift()

    cAnimation = Canvas(animation, width=size, height=size, bg="#282828")
    cAnimation.pack(fill=BOTH)
    cAnimation.images = [ImageTk.PhotoImage(img.resize((size, size))) for img in GENERATED]
    if get_num_fps() != 0:
        cAnimation.delay = int(1/get_num_fps()*1000)
        cAnimation.after(cAnimation.delay, next_animation, cAnimation)

    cAnimation.cpt = 0
    cAnimation.create_image(0, 0, image=cAnimation.images[cAnimation.cpt], anchor=NW)


def convert_array_to_img(arr):
    return Image.fromarray(numpy.array(arr).astype('uint8'), 'RGB')


def generate():
    solutions = []
    LED = get_num_led()
    COLOR_FACTOR = get_num_color_compression()
    COLOR_COMPRESS = COLOR_FACTOR > 1
    SAMPLING_SIZE = get_num_sampling()
    clear_generated()
    MAX = len(IMAGES)
    n = 1
    progress["value"] = 0
    window.update()
    code_array = []
    colors = {}
    for image in IMAGES:
        img = numpy.array(image)
        solutions.append(compute(img, LED, COLOR_COMPRESS, COLOR_FACTOR, sampling_size=SAMPLING_SIZE, c=(40,40,40), bit3=is_3bit()))
        GENERATED.append(convert_array_to_img(solutions[len(solutions)-1][2]))
        code_array.append(generate_code_array(solutions[n-1][1], colors))
        progress["value"] = int(n*100/MAX)
        progress.update()
        n += 1
        draw_all_generated_images()
    if n > 1:
        generate_code(n-1, code_array, solutions[0][3], colors)
        print(CODE)


def generate_code_array(image, colors):
        code = "{"
        for pixel in image[:-1]:
            color = "CRGB(%s, %s, %s)" % (pixel[0], pixel[1], pixel[2])
            if color not in colors:
                colors[color] = len(colors)
            code += "%s, " % colors[color]
        pixel = image[len(image)-1]
        color = "CRGB(%s, %s, %s)" % (pixel[0], pixel[1], pixel[2])
        if color not in colors:
            colors[color] = len(colors)
        code += "%s" % colors[color]
        return code+"}"


CODE = ""
def generate_code(n, images, positions, colors):
    global CODE
    CODE = "#define NUM_LEDS %s\n" % (len(positions)-1)
    CODE += "#define N_IMAGES %s\n" % n
    CODE += "const int POSITIONS[%s] = %s;\n" % (len(positions), str(positions).replace("[", "{").replace("]", "}"))
    CODE += "const int PIXELS[N_IMAGES][%s] = {\n" % (positions[len(positions)-1])
    for i in range(len(images)):
        image = images[i]
        CODE += "\t" + image
        if i == len(images)-1:
            CODE += "\n"
        else:
            CODE += ",\n"
    CODE += "};\n"
    colors_value = str(colors.keys()).replace("dict_keys([", "{").replace("])", "}").replace("'", "")
    CODE += "const CRGB COLORS[%s] = %s;\n" % (len(colors), colors_value)


def save_code():
    if CODE != "":
        file = tkinter.filedialog.asksaveasfile(
            title="Save as...",
            initialfile="image",
            mode='w',
            defaultextension=".h",
            filetypes=[('Header files', '.h'), ('all files', '.*')]
        )
        if file is not None:
            code = CODE
            if get_num_fps() > 0:
                code += "const float IMAGE_TIME = %s;\n" % (1.0/get_num_fps()*1000)
            else:
                code += "const float IMAGE_TIME = 0;\n"
            file.write(code)
            file.close()


###################
BOTTOM_BUTTONS = Frame(window, cnf=frameCnf, bg="#2b2b2b")
bGenerate = Button(BOTTOM_BUTTONS, text="Generate", command=generate, cnf=cnfButtons, bg="#1e8449", fg="white", activebackground="#81c784")
bPlay = Button(BOTTOM_BUTTONS, text="Play", command=play_animation, cnf=cnfButtons, bg="#1e8449", fg="white", activebackground="#81c784")
bSave = Button(BOTTOM_BUTTONS, text="Save", command=save_code, cnf=cnfButtons, bg="#1e8449", fg="white", activebackground="#81c784")
bGenerate.pack(expand=True, fill=X, side=LEFT, padx=10, pady=8)
bPlay.pack(side=LEFT, padx=10, pady=8)
bSave.pack(side=LEFT, padx=10, pady=8)
###################


MENU_TOP.pack(side=TOP, fill=X)
IMAGE_PREVIEW.pack(fill=X, pady=8)
INPUT.pack(anchor=CENTER, fill=X)
IMAGE_GENERATED.pack(fill=X, pady=8)
BOTTOM_BUTTONS.pack(fill=X, pady=8)

progress.pack(expand=True, fill=BOTH, side=TOP)
progress["value"] = 0

window.mainloop()