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
button_identities = []
image_button_id = []
img_identity = []
label_identities = []
tagkeys = []
master = Tk()
image_tags = []
width = 1920
height = 1080
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
    global button_identities, image_tags, temp
    count = 0
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

    tagsframe.grid(row=1, column=0, sticky=NSEW, columnspan=11)


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
    list_tags()
    global img_identity, position, loaded, namenoises, pics, pic_info, temp
    name = ''
    # Create a function to check if the name has been created for that photo yet

    dir = "pics_here"
    pics = os.listdir(dir)
    pics.sort()
    for i in pics:
        temp = [i, gen_name()]
        pic_info.append(temp)

    temp = pic_info[position]
    draw_images(0)


# this function was made in the hopes that i could make the program slightly more efficient,
# and it fucking does, suck my ass.
def draw_images(newpos):
    global img_identity, arrow_identity, pics, image_button_id

    image_canvas = Canvas(master, bd=0)
    images_frame = Frame(image_canvas, width=1900, height=500)
    yscrollbar = Scrollbar(master, orient=VERTICAL, command=image_canvas.yview())
    image_canvas.configure(yscrollcommand=yscrollbar.set)

    yscrollbar.grid(row=3, column=1, sticky=N + S)

    # images_frame.grid(row=3, column=0)

    yscrollbar.config(command=image_canvas.yview)

    image_canvas.config(width=1920, height=500, scrollregion=image_canvas.bbox("all"))
    image_canvas.config(yscrollcommand=yscrollbar.set)
    image_canvas.grid(row=3, column=0, sticky=N + S + E + W)

    images_frame.bind("<Configure>", lambda event, canvas=image_canvas:canvas.configure(scrollregion=image_canvas.bbox("all")))

    # scrollbar = Scrollbar(master)
    # scrollbar.grid(sticky=NS)

    fetch_data(newpos)
    row = 4
    col = 0

    if len(img_identity) > 0:
            bname = (img_identity[0])
            bname.destroy()
            img_identity = []
            for i in range(1, len(arrow_identity)):
                bname = arrow_identity[i]
                bname.destroy()
                arrow_identity = []
    for i in range(0, len(pics)):
        image = Image.open("Pics_here/%s" % (pics[i]))

        # resizing function starts
        w = image.width
        h = image.height
        multiplier = 0
        ratio = Fraction(w, h)
        e = str(ratio).split('/')
        print('resizing {}, fractoin is {}'.format(pics[i], e))
        if len(e) != 1:
            width_r = int(e[0])
            height_r = int(e[1])
            bigger = 'h' if h > w else 'w'

            if bigger == 'w':
                multiplier = 100 / width_r

            elif bigger == 'h':
                multiplier = 100 / height_r

            new_w = int(multiplier * width_r)
            new_h = int(multiplier * height_r)
        else:
            new_w = 100
            new_h = 100
            bigger = 'image was 1:1'

        print("resizing: {}x{} to {}x{} scaled by {} ({})".format(w, h, new_w, new_h, int(multiplier), bigger))
        print()
        image = image.resize((new_w, new_h), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        label = Label(image=photo)
        label.image = photo
        label.grid(in_=image_canvas, row=row, column=col)
        img_identity.append(label)
        image.close()

        button = Button(master, text=pics[i], command=partial(open_full, i))
        image_button_id.append(button)
        button.grid(in_=image_canvas, column=col, row=row + 1, sticky=NSEW)

        col += 2
        if col >= 6:
            col = 0
            row += 2
    # resizing function ends


# Generates the new position, This is done though making the list cyclic rather than linear
def change_pos(func):
    global position, img_identity, arrow_identity
    dir = os.listdir("Pics_here")
    print(func)
    if func == 0:
        position = position - 1
        if position < 0:
            position = len(dir) - 1
    elif func == 1:
        position = position + 1
        if position > len(dir) - 1:
            position = 0
    print()
    print("changed pos variable to {}".format(position))
    #change_image(position)
    list_tags()


# This is supposed to save and fetch the new info for the next image
def fetch_data(newpos):
    global temp, pic_info, position, name_s, tagsext_s, tagsext
    for e in pic_info:
        index = str(e).find(temp[1])
        if index > 0:
            old_pos = pic_info.index(e)
            print(old_pos)

    pic_info[old_pos] = temp
    temp = pic_info[newpos]
    name_s = temp[1]
    #apply_ntags(-1)


# open image full size
def open_full(index):
    global position, loaded, pics
    pos = position
    if len(pics) > 0:
        dir = "pics_here"
        pics = os.listdir(dir)
        pics.sort()
        master.geometry("%sx%s" % (1200, 900))
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
filemenu.add_command(label="Load images", command=open_images())
filemenu.add_separator()

filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)

debugmenu = Menu(master, tearoff=0)
debugmenu.add_command(label="Print all possible", command=partial(print, tags))
debugmenu.add_command(label="Delete data.txt", command=clear_data)
menubar.add_cascade(label="debug", menu=debugmenu)

master.config(menu=menubar)

master.geometry("%sx%s" % (width, height))

toolsframe = Frame(master=None)

toolsframe.grid()

# button = Button(master, text='open full size', command=open_full)
# button.grid(in_=toolsframe, sticky=EW, row=1, column=3)

master.mainloop()
