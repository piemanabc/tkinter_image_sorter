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

image_tags = []
width = 1200
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
def add_tag(window, entry):
    tag = entry.get().lower()
    if tags.count(tag) > 0:
        error_popup("Tag conflict!", "Already added tag!")
    else:
        tags.append(tag)
        print("added tag: %s" % (entry.get()))
        list_tags(window)
    entry.delete(0, END)


#############################################################################################
# ////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #
#                        THIS FUNCTION IS NOW REDUNDANT DO NOT CALL IT                      #
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////////////////////////////// #
#############################################################################################
def apply_tag(n):
    global namenoises, pic_info, position
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



# removes tag from image
def remove_tag(n):
    global tags, image_tags, position, temp
    temp = pic_info[position]
    rem = tags[n]
    temp.pop(temp.index(rem))
    apply_ntags(-1)
    bname = neg_button_identities[n]
    bname.configure(state=DISABLED)
    bname = pos_button_identities[n]
    bname.configure(state=ACTIVE)


# remove tag from list
# ###################################################
# ##### This needs some work with the new system ####
# ###################################################

def delete_tag(n, window):
    global tags, pic_info, temp
    tag = tags[n]
    for e in pic_info:
        index = e.count(tags[n])
        if index > 0:
            e.pop(index)

    tags.pop(tags.index(tag))
    print("removed {}".format(tags[n]))
    apply_ntags(-1)
    list_tags(window)



# list all tags for user to see, this may need to be reworked
def list_tags(window):
    global button_identities, pos_button_identities, neg_button_identities, rem_button_identities, image_tags, temp
    count = 0
    tagsframe = Frame(master=None)
    tagsframe.grid(row=1, column=0, sticky=NSEW, columnspan=4)

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
        button = Button(window, image=ico, command=partial(apply_ntags, i))
        pos_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=0, sticky=NSEW)
        label = Label(image=ico)
        label.image = ico

        label = Label(window, text=tags[i])
        label_identities.append(label)
        label.grid(in_=tagsframe, row=row, column=1, sticky=NSEW)

        ico = PhotoImage(file='ico/-.png')
        button = Button(window, text=tags[i], image=ico, command=partial(remove_tag, i))
        neg_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=2, sticky=NSEW)
        n = len(neg_button_identities) - 1
        label = Label(image=ico)
        label.image = ico
        bname = neg_button_identities[n]
        bname.configure(state=DISABLED)

        ico = PhotoImage(file='ico/X.png')
        button = Button(window, text=tags[i], image=ico, command=partial(delete_tag, i, window))
        rem_button_identities.append(button)
        button.grid(in_=tagsframe, row=row, column=3, sticky=NSEW)
        label = Label(image=ico)
        label.image = ico

        count += 1
        row += 1

    if len(temp) > 1:
        for e in range(0, len(tags)):
            if temp.count(tags[e]) > 0:
                bname = pos_button_identities[e]
                bname.configure(state=DISABLED)
                bname = neg_button_identities[e]
                bname.configure(state=ACTIVE)


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
    global tags, temp, tagsext, tagsext_s

    if place > -1:
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

        error_popup('image saved!', 'Saved the name {}!'.format(name))


# load in all images, this function is loaded every fucking time the position is changed
# that is quite possibly the LEAST efficient way of doing this. what the fuck is wrong with you
def open_images(window,frame):
    list_tags(window)
    global img_identity, arrow_identity, position, loaded, namenoises, pics, pic_info, temp
    name = ''
    namenoises = Label(window, text=name)

    namenoises.grid(in_=frame, sticky=NSEW, row=3, column=3)
    # Create a function to check if the name has been created for that photo yet

    dir = "pics_here"
    pics = os.listdir(dir)
    print(pics)

    for item in pics:
        if os.path.isdir('{}/{}'.format(dir, item)):
            pics.pop(pics.index(item))

    print(pics)

    pics.sort()
    for i in pics:
        temp = [i, gen_name()]
        pic_info.append(temp)

    temp = pic_info[position]

    change_image(0, window)


# this function was made in the hopes that i could make the program slightly more efficient,
# and it fucking does, suck my ass.
def change_image(newpos, window):
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
    height_r = int(e[-1])
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
        button = Button(window, text=tags[i], image=ico, command=partial(change_pos, i, window))
        arrow_identity.append(button)
        neg_button_identities.append(button)
        button.grid(row=1, column=5 + (i * 2), sticky=NSEW)
        label = Label(image=ico)
        label.image = ico


# Generates the new position, This is done though making the list cyclic rather than linear
def change_pos(func, window):
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
    change_image(position, window)
    list_tags(window)


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
    apply_ntags(-1)


def hello_world():
    print("oi cunt")


# open image full size
def open_full(window):
    global position, loaded
    pos = position
    if len(arrow_identity) > 0:
        dir = "pics_here"
        pics = os.listdir(dir)
        pics.sort()
        window.geometry("%sx%s" % (1200, 900))
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
        error_popup('Load images!', "Please choose File > Load images")

for item in ascii_uppercase:
    alphabet.append(item)

read_config()

