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
loaded = FALSE
tags_e = ''
name = ''
name_s = ''
namenoises = ''
pics = []
pic_info = []

tagsext = ''

# this is part of the thing i just broke


# This function updates teh label with a preview of the name
def name_update(label):
    def namecheck():
        global name, tags_e, pic_info, position
        temp = pic_info[position]
        label.config(text=str(temp[1]))
        label.after(10, namecheck)
    namecheck()


# debug option
def print_all(array):
    print(array)


# adding a tag to a the list of tags
def add_tag():
    print("added tag: %s" % (e1.get()))
    temp = e1.get()
    tags.append(temp)
    e1.delete(0, END)


#############################################################################################
# ////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
#                        THIS FUNCTION IS NOW REDUNDANT DO NOT CALL IT                      #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////////////////////////////// #
#############################################################################################
def apply_tag(n):
    global namenoises, pic_info, position, wantedt
    print(n)
    # temp = pic_info[position]
    if len(temp) < 3:
        temp.append(tags[n])
        print("no tags so i added some")
    else:
        print(temp)
        temp.append(tags[n])
        print(temp)
    bname = (pos_button_identities[n])
    image_tags.append(tags[n])
    bname.configure(text="added", state=DISABLED)
    bname = neg_button_identities[n]
    bname.configure(state=ACTIVE)
    gen_name()
    name_update(namenoises)
    # also part of the broken thing
    wantedt.append(n)


# removes tag from image
def remove_tag(n):
    global tags, image_tags, position, temp
    temp = pic_info[position]
    rem = tags[n]
    print(temp)
    temp.pop(temp.index(rem))
    print(temp)
    bname = neg_button_identities[n]
    bname.configure(state=DISABLED)
    bname = pos_button_identities[n]
    bname.configure(state=ACTIVE)


# remove tag from list
# ###################################################
# ##### This needs some work with the new system ####
# ###################################################
def delete_tag(n):
    global tags, image_tags
    print("removed {}".format(tags[n]))
    tag = tags[n]

    tags.pop(tags.index(tag))
    image_tags.pop(image_tags.index(tag))

    list_tags()


# list all tags for user to see, this may need to be reworked
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
    row = 0
    for i in range(0, len(tags)):
        # attempting to integrate apply_ntags into program
        ico = PhotoImage(file='ico/tick.png')
        button = Button(master, image=ico, command=partial(apply_ntags, i))
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


# saves the list ofb tags to a file
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


# this applys the tags to the name, encoding them as strs
# this array expects a list to be given then iterates though it
# this may be the best option for saving the names of teh files with the preview removed
# this is the broken thing, It goes into a infinite loop
def apply_ntags(place):
    global tags, temp, tagsext
    temp.append(tags[place])
    tagsext = []

    for index_temp in range(2, len(temp)):
        index_tags = tags.index(temp[index_temp])
        tagsext.append(alphabet[index_tags])

    tagsext.sort()
    tagsext_s = ''
    for item in tagsext:
        tagsext_s = tagsext_s + item

    bname = (pos_button_identities[place])
    image_tags.append(tags[place])
    bname.configure(text="added", state=DISABLED)
    bname = neg_button_identities[place]
    bname.configure(state=ACTIVE)


# saves the name of the image to the image. Currently not working
def save_name(name):

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


# load in all images, this function is loaded every fucking time the position is changed
# that is quite possibly the LEAST efficient way of doing this. what the fuck is wrong with you
def open_images():
    list_tags()
    global img_identity, arrow_identity, position, loaded, namenoises, pics, pic_info, temp
    name = ''
    namenoises = Label(master, text=name)

    namenoises.grid(in_=toolsframe, sticky=NSEW, row=3, column=3)
    # Create a function to check if the name has been created for that photo yet

    dir = "pics_here"
    pics = os.listdir(dir)
    pics.sort()
    for i in pics:
        temp = [i, gen_name()]
        pic_info.append(temp)

    temp = pic_info[position]
    master.geometry("%sx%s" % (1200, 900))
    change_image(0)


# this function was made in the hopes that i could make the program slightly more efficient,
# and it fucking does, suck my ass.
def change_image(newpos):
    global img_identity, arrow_identity, loaded, namenoises, pics, position

    fetch_data(newpos)

    if len(img_identity) > 0:
            bname = (img_identity[0])
            bname.destroy()
            img_identity = []
            for i in range(1, len(arrow_identity)):
                bname = arrow_identity[i]
                bname.destroy()
                arrow_identity = []

    image = Image.open("Pics_here/%s" % (pics[newpos]))
    name_update(namenoises)
# resizing function starts
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
    image.close()

    # resizing function ends


    for i in range(0, 2):
        ico = PhotoImage(file=arrows[i])
        button = Button(master, text=tags[i], image=ico, command=partial(change_pos, i))
        arrow_identity.append(button)
        neg_button_identities.append(button)
        button.grid(row=1, column=5 + (i * 2), sticky=NSEW)
        label = Label(image=ico)
        label.image = ico


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
    change_image(position)


# This is supposed to save and fetch the new info for the next image
def fetch_data(newpos):
    global temp, pic_info, position
    for e in pic_info:
        index = str(e).find(temp[1])
        if index > 0:
            old_pos = pic_info.index(e)
            print(old_pos)

    pic_info[old_pos] = temp
    temp = pic_info[newpos]

# open image full size
def open_full():
    global position, loaded
    pos = position
    if len(arrow_identity) > 0:
        dir = "pics_here"
        pics = os.listdir(dir)
        pics.sort()
        master.geometry("%sx%s" % (1200, 900))
        image = Image.open("Pics_here/%s" % (pics[pos]))
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
        top = Toplevel()
        topframe = Frame(top)

        topframe.grid(row=0, column=0, sticky="NESW")
        topframe.grid_rowconfigure(0, weight=1)
        topframe.grid_columnconfigure(0, weight=1)

        top.geometry("100x100")
        top.title("Load images!")

        msg = Message(top, text="Please choose File > Load images")
        msg.grid(column=3, columnspan=3)

        button = Button(top, text="Dismiss", command=top.destroy)
        button.grid(column=3, columnspan=3)


menubar = Menu(master)


for item in ascii_uppercase:
    alphabet.append(item)

read_config()

filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Refresh tags", command=partial(read_config))
filemenu.add_separator()
filemenu.add_command(label="Save tags", command=save_config)
filemenu.add_command(label="Save tags to image", command=save_name)
filemenu.add_command(label="Load images", command=open_images)
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

button = Button(master, text='open full size', command=open_full)
button.grid(in_=toolsframe, sticky=EW, row=0, column=3)

Label(master, text="Current name:").grid(in_=toolsframe, sticky=NSEW, row=2, column=3)

button = Button(master, text='Apply!', command=save_name)
button.grid(in_=toolsframe, sticky=EW, row=6, column=3)

master.mainloop()
