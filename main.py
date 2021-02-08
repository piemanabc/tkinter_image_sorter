


from script.Read_names import *
#from script.Write_names import *

sys.path.insert(0,  'D:/Python/tkinter_image_sorter/script/')
temp_parent = []
master = Tk()


def write_tags(window):
    menubar = Menu(window)

    for item in ascii_uppercase:
        alphabet.append(item)

    read_config()

    toolsframe = Frame(master=None)
    filemenu = Menu(window, tearoff=0)
    filemenu.add_command(label="Refresh tags", command=partial(read_config))
    filemenu.add_separator()
    filemenu.add_command(label="Save tags", command=save_config)
    filemenu.add_command(label="Save tags to image", command=save_name)
    filemenu.add_command(label="Load images", command=partial(open_images, window, toolsframe))
    filemenu.add_separator()
    filemenu.add_command(label="List all tags", command=list_tags)
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="Tags", menu=filemenu)

    debugmenu = Menu(window, tearoff=0)
    debugmenu.add_command(label="Print all possible", command=partial(print, tags))
    debugmenu.add_command(label="Print all applied", command=partial(print_all, image_tags))
    debugmenu.add_command(label="Delete data.txt", command=clear_data)
    menubar.add_cascade(label="debug", menu=debugmenu)

    window.config(menu=menubar)

    window.geometry("%sx%s" % (width, height))

    Label(window, text="enter tags").grid(in_=toolsframe, sticky=NSEW, row=0, column=0)

    e1 = Entry(window)
    e1.grid(in_=toolsframe, row=0, sticky=NSEW, columnspan=1, column=1)

    button = Button(window, text='add', command=partial(add_tag, window, e1))
    button.grid(in_=toolsframe, sticky=EW, row=0, column=3)

    toolsframe.grid()

    button = Button(window, text='open full size', command=open_full)
    button.grid(in_=toolsframe, sticky=EW, row=1, column=3)

    Label(window, text="Current name:").grid(in_=toolsframe, sticky=NSEW, row=2, column=3)

    button = Button(window, text='Apply!', command=save_name)
    button.grid(in_=toolsframe, sticky=EW, row=6, column=3)


def read_tags(window):

    for item in ascii_uppercase:
        alphabet.append(item)

    read_config()
    toolsframe = Frame(master=None)

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

    toolsframe.grid()

menubar = Menu(master)


filemenu = Menu(master, tearoff=0)
filemenu.add_command(label="Read tags", command=partial(read_tags, master))
filemenu.add_command(label="Write tags", command=partial(write_tags, master))
filemenu.add_separator()

filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)


master.config(menu=menubar)
master.geometry("%sx%s" % (300, 300))


master.mainloop()
