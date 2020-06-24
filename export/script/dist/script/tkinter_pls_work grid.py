from tkinter import *
from functools import partial
import os
from PIL import Image, ImageTk
from string import ascii_uppercase
from random import randint
from fractions import Fraction


alphabet = []
config_index = ['tags', 'tagkeys']
tags = []
arrow_identity = []
button_identities = []
rem_button_identities = []
pos_button_identities = []
neg_button_identities = []
img_identity = []
label_identities = []
tagkeys = []
master = Tk()
image_tags = []
width = 350
height = 97
position = 0
del_count = 0


def print_all(array):
    print(array)


def add_tag():
    print("added tag: %s" % (e1.get()))
    temp = e1.get()
    tags.append(temp)
    e1.delete(0, END)


def apply_tag(n):
    bname = (pos_button_identities[n])
    image_tags.append(tags[n])
    bname.configure(text="added", state=DISABLED)
    bname = neg_button_identities[n]
    bname.configure(state=ACTIVE)


def remove_tag(n):
    global tags, image_tags
    str = (tags[n])
    if image_tags.index(str):
        location = image_tags.index(str)
        image_tags.pop(location)
    bname = neg_button_identities[n]
    bname.configure(state=DISABLED)
    bname = pos_button_identities[n]
    bname.configure(state=ACTIVE)
    print(button_identities)


def delete_tag(n):
    global tags, image_tags, neg_button_identities, pos_button_identities, rem_button_identitiese, label_identities, del_count
    print("index:{}, tags:{}, del_count:{}".format(n, tags ,del_count))
    tag = tags[n]

    tags.pop(tags.index(tag))

    list_tags()


def list_tags():
    count = 0
    tagsframe = Frame(master=None)
    tagsframe.grid(row=1, column=0, sticky=NSEW, columnspan=4)
    global button_identities, pos_button_identities, neg_button_identities, rem_button_identities, image_tags
    if len(button_identities) > 0:

        for index, item in range(0, len(pos_button_identities)):
            bname = (pos_button_identities[index])
            bname.destroy()
        for index, item in range(0, len(neg_button_identities)):
            bname = (neg_button_identities[index])
            bname.destroy()
        for index, item in range(0, len(rem_button_identities)):
            bname = (rem_button_identities[index])
            bname.destroy()
        for index, item in range(0, len(label_identities)):
            bname = (label_identities[index])
            bname.destroy()

    button_identities = []
    neg_button_identities = []
    pos_button_identities = []
    rem_button_identities = []
    row = 3

    for i in range(0, len(tags)):
        ico = PhotoImage(file='ico/tick.png')
        button = Button(master, image=ico, command=partial(apply_tag, i))
        pos_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=0, sticky=NSEW)
        label = Label(image=ico)
        label.image = ico

        label = Label(master, text=tags[i])
        label_identities.append(label)
        label.grid(in_=tagsframe, row=row, column=1, sticky=NSEW)

        ico = PhotoImage(file='ico/-.png')
        button = Button(master, text=tags[i], image=ico, command=partial(remove_tag, i))
        neg_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=2, sticky=NSEW)
        n = len(neg_button_identities) - 1
        label = Label(image=ico)
        label.image = ico
        bname = neg_button_identities[n]
        bname.configure(state=DISABLED)

        ico = PhotoImage(file='ico/X.png')
        button = Button(master, text=tags[i], image=ico, command=partial(delete_tag, i))
        rem_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=3, sticky=NSEW)
        label = Label(image=ico)
        label.image = ico

        if any(tags[i] in s for s in image_tags):
            bname = pos_button_identities[i]
            bname.configure(state=DISABLED)
            bname = neg_button_identities[i]
            bname.configure(state=ACTIVE)
        count += 1
        row += 1


def save_config():
    global tags
    global tagkeys
    print("saving tags")
    lines = []
    for i, item in enumerate(config_index):
        if i == 0:  # line 1
            string = tags
            final = str(item + '=')
            for a, s_item in enumerate(string):
                blank = '' if a == 0 else ', '
                final = str(final + blank + s_item)
            lines.append(final)

        if i == 1:  # line 2
            string = tagkeys
            final = str(item + '=')
            for a, s_item in enumerate(string):
                blank = '' if a == 0 else ', '
                final = str(final + blank + s_item)
                print(final)
                lines.append(final)

    if not os.path.exists('data/config.ini'):
        file = open("data/config.ini", 'x')
    else:
        file = open("data/config.ini", "r+")
    print(lines)
    for i, item in enumerate(lines):
        file.writelines(lines[i])
        file.writelines("\n")

    print("tags saved")


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


def clear_data():
    os.remove('data/config.ini')
    print("removed saved tags")


def save_name():
    name = ''
    for item in range(0, 5):
        num = randint(0, 9)
        name = str(name) + str(num)

    for index, item in enumerate(tags):
        if item in image_tags:
            location = tags.index(item)
            name = name + str(alphabet[location])

    top = Toplevel()
    topframe = Frame(top)

    topframe.grid(row=0, column=0, sticky="NESW")
    topframe.grid_rowconfigure(0, weight=1)
    topframe.grid_columnconfigure(0, weight=1)

    top.geometry("150x150")
    top.title("Image saved!")

    msg = Message(top, text="saved image as {} \n (this is temporary, i actually did nothing)".format(name))
    msg.grid(column=3, columnspan=3)

    button = Button(top, text="Dismiss", command=top.destroy)
    button.grid(column=3, columnspan=3)


def open_images(pos):
    list_tags()
    global img_identity, arrow_identity
    if len(img_identity) > 0:
            bname = (img_identity[0])
            bname.destroy()
            img_identity = []
            for i in range(1, len(arrow_identity)):
                bname = arrow_identity[i]
                bname.destroy()
                arrow_identity = []
    dir = "pics_here"
    pics = os.listdir(dir)
    pics.sort()
    master.geometry("%sx%s" % (1200, 900))
    image = Image.open("Pics_here/%s" % (pics[pos]))
    w = image.width
    h = image.height
    multiplier = 0
    ratio = Fraction(w, h)
    e = str(ratio).split('/')
    width_r = int(e[0])
    height_r = int(e[1])
    bigger = 'h' if h > w else 'w'

    if bigger == 'w':
        multiplier = 900 / width_r

    elif bigger == 'h':
        multiplier = 500 / height_r

    new_w = int(multiplier * width_r)
    new_h = int(multiplier * height_r)

    print("resizing: {}x{} to {}x{} scaled by {} ({})".format(w, h, new_w, new_h, int(multiplier), bigger))
    image = image.resize((new_w, new_h), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    label = Label(image=photo)
    label.image = photo
    label.grid(sticky=NE, row=1, column=6)
    img_identity.append(label)
    arrows = ['ico/lefta.png', 'ico/righta.png']

    for i in range(0, 2):
        ico = PhotoImage(file=arrows[i])
        button = Button(master, text=tags[i], image=ico, command=partial(change_pos, i))
        arrow_identity.append(button)
        neg_button_identities.append(button)
        button.grid(row=1, column=5+(i*2), sticky=NSEW)
        label = Label(image=ico)
        label.image = ico


def change_pos(func):
    global position
    dir = os.listdir("Pics_here")
    if func == 0:
        position = position - 1
        if position < 0:
            position = len(dir) - 1
    elif func == 1:
        position = position + 1
        if position > len(dir) - 1:
            position = 0
    open_images(position)


menubar = Menu(master)

for item in ascii_uppercase:
    alphabet.append(item)

read_config()

filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Refresh tags", command=partial(read_config))
filemenu.add_separator()
filemenu.add_command(label="Save tags", command=save_config)
filemenu.add_command(label="Save tags to image", command=save_name)
filemenu.add_command(label="Load images", command=partial(open_images, position))
filemenu.add_separator()
filemenu.add_command(label="List all tags", command=list_tags)
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)

debugmenu = Menu(master, tearoff=0)
debugmenu.add_command(label="Print all possible", command=partial(print, tags))
debugmenu.add_command(label="Print all applied", command=partial(print_all, image_tags))
debugmenu.add_command(label="Delete data.txt", command=clear_data)
menubar.add_cascade(label="debug", menu=debugmenu)

master.config(menu=menubar)

master.geometry("%sx%s" % (width, height))

toolsframe = Frame(master=None)
Label(master, text="enter tags").grid(in_=toolsframe, sticky=NSEW, row=0, column=0)

e1 = Entry(master)
e1.grid(in_=toolsframe, row=0, sticky=NSEW, columnspan=1, column=1)

button = Button(master, text='add', command=add_tag)
button.grid(in_=toolsframe, sticky=EW, row=0, column=3)
toolsframe.grid()

master.mainloop()
