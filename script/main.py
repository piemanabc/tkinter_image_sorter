from tkinter import *
import sys
from functools import partial

from script.Read_names import *

#from script.Write_names import *

sys.path.insert(0,  'D:/Python/tkinter_image_sorter/script/')
temp_parent = []
master = Tk()


def write_tags():
    print("I haven't programmed that path yet")


def read_tags(window):

    for item in ascii_uppercase:
        alphabet.append(item)

    read_config()

    filemenu = Menu(window, tearoff=0)
    filemenu.add_command(label="Load tags", command=partial(read_config))
    filemenu.add_command(label="Load images", command=partial(open_images, window))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)

    menubar.add_cascade(label="Load", menu=filemenu)

    debugmenu = Menu(window, tearoff=0)
    debugmenu.add_command(label="Print all possible", command=partial(print, tags))
    debugmenu.add_command(label="show me a error", command=partial(error_popup, 'title', 'this is a test \n Fuck me'))
    debugmenu.add_command(label="Delete data.txt", command=clear_data)
    menubar.add_cascade(label="debug", menu=debugmenu)

    window.config(menu=menubar)

    window.geometry("%sx%s" % (width, height))

    toolsframe = Frame(master=None)

    toolsframe.grid()



menubar = Menu(master)


filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Read tags", command=partial(read_tags, master))
filemenu.add_command(label="Write tags", command=write_tags)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)


master.config(menu=menubar)
master.geometry("%sx%s" % (300, 300))
'''
label = Label(master, text="Would you like to sort or view images?")
label.grid(in_=master, sticky=NSEW)
temp_parent.append(label)

button = Button(master, text='Write', command=write_tags)
button.grid(in_=master, sticky=EW, row=3)
temp_parent.append(button)

button = Button(master , text='Read', command=read_tags)
button.grid(in_=master, sticky=EW, row=5)
temp_parent.append(button)

'''
master.mainloop()
