from tkinter import *
import sys
from functools import partial

sys.path.insert(0,  'D:/Python/tkinter_image_sorter/script/')
temp_parent = []


def write_tags():
    for item in temp_parent:
        item.destroy()
    from script import Write_names
    parent.self.destroy()


def read_tags():
    for item in temp_parent:
        item.destroy()
    from script import Read_names
    parent.self.destroy()

parent = Tk()

parent.geometry("%sx%s" % (300, 300))

label = Label(parent, text="Would you like to sort or view images?")
label.grid(in_=parent, sticky=NSEW)
temp_parent.append(label)

button = Button(parent, text='Write', command=write_tags)
button.grid(in_=parent, sticky=EW, row=3)
temp_parent.append(button)

button = Button(parent, text='Read', command=read_tags)
button.grid(in_=parent, sticky=EW, row=5)
temp_parent.append(button)

parent.mainloop()
