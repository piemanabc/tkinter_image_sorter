from tkinter import *
from functools import partial
import os
from PIL import Image, ImageTk
from string import ascii_uppercase
from random import randint
from fractions import Fraction
from math import ceil


alphabet = []
config_index = ['tags', 'tagkeys']
tags = []
button_identities = []
image_identities = []
image_button_id = []
label_identities = []
arrow_identity = []
tagkeys = []
master = Tk()
image_tags = []
width = 1675
height = 900
position = 0
del_count = 0
loaded = FALSE
tags_e = ''
name = ''
name_s = ''
namenoises = ''
pics = []
pic_info = []
temp = []
tagsext_s = ''
tagsext = ''
rows = 0
arrows = ['ico/lefta.png', 'ico/righta.png']
img_dir = 'D:/Python/tkinter_image_sorter/script/Pics_here'

button_test = ''


def error_popup(title, errortxt):
    top = Toplevel()
    topframe = Frame(top)

    topframe.grid(row=0, column=0, sticky="NESW")
    topframe.grid_rowconfigure(0, weight=1)
    topframe.grid_columnconfigure(0, weight=1)

    top.geometry("300x300")
    top.title(title)

    msg = Message(top, text=errortxt)
    msg.grid(column=3, columnspan=3)

    button = Button(top, text="Okay", command=top.destroy)
    button.grid(column=3, columnspan=3)


def add_filter(item, index):
    print('adding filter {} from position {}'.format(item, index))
    button = button_identities[index]
    button.configure(command=partial(rem_filter, item, index), relief=SUNKEN)


def rem_filter(item, index):
    print('Removing filter {} from position {}'.format(item, index))
    button = button_identities[index]
    button.configure(command=partial(add_filter, item, index), relief=RAISED)


# list all tags for user to see, this may need to be reworked
def list_tags():
    global button_identities, arrow_identity, image_tags, temp, arrows, pics
    count = 0
    num_pages = int(ceil(len(pics) / 10))
    print(len(pics))
    button_identities = []
    col = 2

    tagsframe = Frame(master=None)
    Label(master, text="Current tags:  ").grid(in_=tagsframe, sticky=NSEW, row=1, column=1)

    for i in range(0, len(tags)):
        button = Button(master, text=tags[i], command=partial(add_filter, tags[i], i))
        button_identities.append(button)
        button.grid(in_=tagsframe, column=col+1, row=1, sticky=NSEW)

        count += 1
        col += 1

    tagsframe.grid(row=0, column=0, sticky=NSEW, columnspan=len(tags) + 2)

    page_mover_frame = Frame(master=None)

    button = Button(master, text='Back a page', command=partial(print, 'Back a page'))
    button.grid(in_=page_mover_frame, row=0, column=0, sticky=NSEW)

    for page in range(num_pages):
        print('made a button')
        button = Button(master, text=page + 1, command=partial(print, page + 1))
        button.grid(in_=page_mover_frame, row=0, column=page + 1, sticky=NSEW)

    button = Button(master, text='forward a page', command=partial(print, 'forward a page'))
    button.grid(in_=page_mover_frame, row=0, column=num_pages + 2, sticky=NSEW)

    page_mover_frame.grid(row=0, column=len(tags)+2, columnspan=num_pages+2,  sticky=NSEW)


# Reads tags and settings from a file from a file
def read_config():
    global tags
    global tagkeys
    if os.path.exists('data/config.ini'):
        print("Reading saved tags")
        global config_index
        with open("data/config.ini", "r") as file:
            for i, line in enumerate(file):
                if i == 0:  # line 1
                    string = line
                    string = string[len(config_index[i]) + 1:-1]
                    string = string.split(", ")
                    tags = string
                if i == 1:  # line 2
                    string = line
                    string = string[len(config_index[i]) + 1:-1]
                    string = string.split(", ")
                    tagkeys = string
    else:
        print("no config found, Please add some tags then save them")


# deletes saved settings
def clear_data():
    os.remove('data/config.ini')
    print("removed saved tags")


# this function is pointless however i want to keep it because
# i cant be bothered fixing what will break if i remove it


# generates a suffix for the image by creating a 5 digit random number
def gen_name():
    global name, namenoises, name_s, tags_e
    name_s = ''
    for item in range(0, 5):
        num = randint(0, 9)
        name_s = str(name_s) + str(num)
    return name_s


def save_name():
    global tagsext_s, name_s, pics

    name = name_s + tagsext_s
    print(name)
    if len(name) < 5:
        error_popup("Load an image!", "please load a image to save it's name!")
    else:
        extension = temp[0].split('.')
        extension.remove(extension[0])
        src = "pics_here/{}".format(temp[0])
        dst = "pics_here/{}.{}".format(name, extension[0])
        print("old name {}".format(dst))
        print("new name {}".format(src))
        os.rename(src, dst)

        print("renamed {} to {}.{}".format(temp[0], name, extension[0]))

        error_popup('image saved!', 'Saved the name {}! (didnt to anything atm)'.format(name))


# load in all images, this function is loaded every fucking time the position is changed
# that is quite possibly the LEAST efficient way of doing this. what the fuck is wrong with you
def open_images():
    global pics, pic_info, img_dir
    # Create a function to check if the name has been created for that photo yet
    pics = os.listdir(img_dir)
    pics.sort()
    list_tags()
    draw_images()


# this function was made in the hopes that i could make the program slightly more efficient,
# and it fucking does, suck my ass.
def draw_images():
    global image_identities, button_identities, pics, image_button_id, img_dir

    # attach scroll action to scrollbar
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    if len(image_identities) > 0:
        for item in range(0, len(image_identities)):
            image = (image_identities[item])
            image.destroy()
        image_identities = []
        for item in range(0, len(button_identities)):
            btn = (button_identities[item])
            btn.destroy()
        button_identities = []

    canvas = Canvas(master, borderwidth=0)
    frame = Frame(canvas)
    vsb = Scrollbar(master, orient="vertical", command=canvas.yview)

    canvas.configure(yscrollcommand=vsb.set)

    vsb.grid(in_=frame, row=0, column=9, sticky=N + S)
    canvas.grid(column=0, row=5)
    canvas.create_window((4, 4), window=frame, anchor=NW)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    row = 0
    col = 0
    global rows
    for item in range(0, len(pics)+1):

        image = Image.open("{}/{}".format(img_dir, pics[item]))

        w = image.width
        h = image.height
        multiplier = 0
        ratio = Fraction(w, h)
        e = str(ratio).split('/')
        print('resizing {}, fractoin is {}'.format(pics[item], e))
        if len(e) != 1:
            width_r = int(e[0])
            height_r = int(e[1])
            bigger = 'h' if h > w else 'w'

            if bigger == 'w':
                multiplier = 200 / width_r

            elif bigger == 'h':
                multiplier = 200 / height_r

            new_w = int(multiplier * width_r)
            new_h = int(multiplier * height_r)
        else:
            new_w = 200
            new_h = 200
            bigger = 'image was 1:1'

        print("resizing: {}x{} to {}x{} scaled by {} ({})".format(w, h, new_w, new_h, int(multiplier), bigger))
        print()
        image = image.resize((new_w, new_h), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        label = Label(image=photo)
        label.image = photo
        image_identities.append(label)
        label.grid(in_=frame, column=col, row=row)
        image.close()

        button = Button(master, text=pics[item], command=partial(open_full, item))
        button.grid(in_=frame, column=col, row=row + 1)

        col += 1

        if col >= 8:
            rows += 4
            col = 0
            row += 2
        if row >= 10:
            print('done')
            break

    vsb.grid(rowspan=rows)


# open image full size
def open_full(index):
    global position, loaded, pics
    pos = position
    if len(pics) > 0:
        dir = "pics_here"
        pics = os.listdir(dir)
        pics.sort()
        image = Image.open("Pics_here/%s" % (pics[index]))
        w = image.width
        h = image.height

        top = Toplevel()
        topframe = Frame(top)

        topframe.grid(row=0, column=0, sticky="NESW")
        topframe.grid_rowconfigure(0, weight=1)
        topframe.grid_columnconfigure(0, weight=1)

        top.geometry("{}x{}".format(w + 20, h + 100))
        top.title("Full Resolution image")

        photo = ImageTk.PhotoImage(image)
        label = Label(topframe, image=photo)
        label.image = photo
        label.grid()

        msg = Message(top)
        msg.grid()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.grid()

    else:
        error_popup('Load images!', "Please choose File > Load images")


menubar = Menu(master)


for item in ascii_uppercase:
    alphabet.append(item)

read_config()

filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Load tags", command=partial(read_config))
filemenu.add_command(label="Load images", command=open_images)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)

debugmenu = Menu(master, tearoff=0)
debugmenu.add_command(label="Print all possible", command=partial(print, tags))
debugmenu.add_command(label="show me a error", command=partial(error_popup, 'title', 'this is a test \n Fuck me'))
debugmenu.add_command(label="Delete data.txt", command=clear_data)
menubar.add_cascade(label="debug", menu=debugmenu)

master.config(menu=menubar)

master.geometry("%sx%s" % (width, height))

toolsframe = Frame(master=None)

toolsframe.grid()

# button = Button(master, text='open full size', command=open_full)
# button.grid(in_=toolsframe, sticky=EW, row=1, column=3)

master.mainloop()
