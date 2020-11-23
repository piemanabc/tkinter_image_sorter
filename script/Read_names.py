from tkinter import *
from functools import partial
import os
from PIL import Image, ImageTk
from string import ascii_uppercase
from random import randint
from fractions import Fraction
from math import ceil
import re


alphabet = []
config_index = ['tags', 'tagkeys']
tags = []
button_identities = []
img_button_identities = []
image_identities = []
image_button_id = []
label_identities = []
arrow_identity = []
drawn_tags = []
tagkeys = []

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
c_page = 0
arrows = ['ico/lefta.png', 'ico/righta.png']
img_dir = 'D:/Python/tkinter_image_sorter/script/Pics_here'
# img_dir = 'D:/back ups/no/i would reccomend staying out of here/lewd'

filtered = []
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


def add_filter(item, index, button, window):
    global temp, alphabet, drawn_tags

    letter = alphabet[index]

    temp.append(letter)
    print(index)
    print()
    print("index is")
    print(temp.index(letter))
    button.configure(command=partial(rem_filter, item, index, button, window), relief=SUNKEN)

    print()
    print('adding filter {} from position {}'.format(item, index))
    print("Setting button {} to SUNKEN".format(button))
    print("inserted tag {}(letter {}) at index {}, list is now {}".format(item, letter,  index, temp))
    print()

    draw_images(window)


def rem_filter(item, index, button, window):
    global temp, alphabet, drawn_tags

    letter = alphabet[index]
    print("removing tag {}(letter {}) at index {}".format(item, letter, index))
    print(temp)
    print()
    button.configure(command=partial(add_filter, item, index, button, window), relief=RAISED)
    temp.pop(temp.index(letter))

    print()
    print('removing filter {} from position {}'.format(item, index))
    print("Setting button {} to RAISED".format(button))

    print(" list is now {}".format(temp))

    draw_images(window)

# list all tags for user to see, this may need to be reworked


def list_tags(window):
    global button_identities, arrow_identity, image_tags, temp, arrows, pics, c_page, num_pages
    count = 0

    # Divide by the number of items per page

    num_pages = int(ceil(len(pics) / 40))
    button_identities = []
    col = 2

    tagsframe = Frame(master=None)

    if num_pages > 0:
        tagsframe.destroy()
        tagsframe = Frame(master=None)

    Label(window, text="Current tags:  ").grid(in_=tagsframe, sticky=NSEW, row=1, column=1)

    for i in range(0, len(tags)):
        button = Button(window, text=tags[i], command=partial(print, "something went wrong"))
        button.configure(command=partial(add_filter, tags[i], i, button, window))
        drawn_tags.insert(i, button)
        button.grid(in_=tagsframe, column=col+1, row=1, sticky=NSEW)

        count += 1
        col += 1

    tagsframe.grid(row=0, column=0, sticky=NSEW, columnspan=len(tags) + 2)

    page_mover_frame = Frame(master=None)

    button = Button(window, text='Back a page', command=partial(change_page, '-', window))
    button.grid(in_=page_mover_frame, row=0, column=0, sticky=NSEW)

    for page in range(num_pages):
        button = Button(window, text=page + 1, command=partial(change_page, page, window))
        if page == c_page:
            button.configure(relief=SUNKEN)
        button.grid(in_=page_mover_frame, row=0, column=page + 1, sticky=NSEW)

    button = Button(window, text='forward a page', command=partial(change_page, '+', window))
    button.grid(in_=page_mover_frame, row=0, column=num_pages + 2, sticky=NSEW)

    page_mover_frame.grid(row=0, column=len(tags)+2, columnspan=num_pages+2,  sticky=NSEW)


# this function needs to change pages, The idea is to make it more like a job queueing type function
#  where it is handed the new data then redraws the page

def change_page(new, window):
    global c_page, num_pages
    print()
    print()
    if new == '-':
        c_page -= 1
        print()
        print("down a page")
    elif new == '+':
        c_page +=1
        print()
        print("up a page")
    else:
        c_page = new
        print()
        print("direct page")

    if c_page > num_pages - 1:
        c_page = 0
    elif c_page < 0:
        c_page = num_pages - 1

    draw_images(window)

    list_tags(window)


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
def open_images(window):
    global pics, pic_info, img_dir
    # Create a function to check if the name has been created for that photo yet
    pics = os.listdir(img_dir)
    pics.sort()
    list_tags(window)
    draw_images(window)


# this function was made in the hopes that i could make the program slightly more efficient,
# and it fucking does, suck my ass.
def draw_images(window):
    global image_identities, button_identities, img_button_identities, pics, image_button_id, img_dir, c_page, rows,\
        temp, filtered

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
        for item in range(0, len(img_button_identities)):
            btn = (img_button_identities[item])
            btn.destroy()

        image_identities = []
        button_identities = []
        img_button_identities = []

    canvas = Canvas(window, borderwidth=0)
    frame = Frame(canvas)
    image_identities.append(frame)
    vsb = Scrollbar(window, orient="vertical", command=canvas.yview)

    canvas.configure(yscrollcommand=vsb.set)

    vsb.grid(in_=frame, row=0, column=9, sticky=N + S)
    canvas.grid(column=0, row=5)
    canvas.create_window((4, 4), window=frame, anchor=NW)

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    row = 0
    col = 0

    print()
    print()
    print("-- Image processing beginning ---")
    print()
    filtered = []
    result = -1
    if len(temp) > 0:
        for tag in temp:
            for pic in pics:
                result = pic.find(tag)
                if result > -1 and not pic in filtered:
                    filtered.append(pic)
    else:
        filtered = pics

    print()
    print("filtered tags")
    print(filtered)
    print()
    print("filtered letters")
    print(temp)
    print()

    if (c_page * 40) + 40 > len(filtered):
        max = len(filtered)
    else:
        max = (c_page * 40) + 40

    for item in range(c_page * 40, max):

        print("{}/{}".format(img_dir, filtered[item]))
        print("This is item {} in the array".format(item))
        image = Image.open("{}/{}".format(img_dir, filtered[item]))

        w = image.width
        h = image.height
        multiplier = 0
        ratio = Fraction(w, h)
        e = str(ratio).split('/')
        print('resizing {}, fraction is {}'.format(filtered[item], e))

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
        button = Button(window, text=filtered[item], command=partial(open_full, item))
        img_button_identities.append(button)
        button.grid(in_=frame, column=col, row=row + 1)

        col += 1

        # 40 items per page
        if col >= 8:
            rows += 4
            col = 0
            row += 2
        if row >= 10:
            print('--- End of image processing ---')
            break
    if rows > 0 :
        vsb.grid(rowspan=rows)


# open image full size
def open_full(index):
    global position, loaded, pics, img_dir, filtered

    if len(pics) > 0:
        pics = os.listdir(img_dir)
        pics.sort()
        image = Image.open("{}/{}".format(img_dir, filtered[index]))
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



#

# button = Button(master, text='open full size', command=open_full)
# button.grid(in_=toolsframe, sticky=EW, row=1, column=3)

