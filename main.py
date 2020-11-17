import tkinter
import os
from logger import logger
import os.path
from copy_tool_function import *


screen = tkinter.Tk()
screen.geometry("500x600")
screen.resizable()
screen.title("Copy tool")

source_frame = tkinter.Frame(screen)
destination_frame = tkinter.Frame(screen, background = "pink")
option_frame = tkinter.Frame(screen, background = "yellow")

source_frame.place(x = 0, y = 0, anchor = "nw", width = 500, height = 220)
destination_frame.place(x = 0, y = 220, anchor = "nw", width = 500, height = 90)
option_frame.place(x = 0, y = 310, anchor = "nw", width = 500, height = 290)

PHONE_ROOT = '/run/user/1000/gvfs/'

def print_source_size():
	checked_phones = []
	for phone in VARIABLE:
		if VARIABLE[phone].get() == 1:
			checked_phones.append(phone)
	size = get_size(checked_phones)
	tkinter.Label(option_frame, 
				  text=size).place(x=120, y=150)


def init_phone(frame):
	starting_x, starting_y = 15, 30
	phones = [phone for phone in os.listdir(PHONE_ROOT) if os.path.isdir(os.path.join(PHONE_ROOT, phone))]
	global VARIABLE
	# Create Checkbutton for phones
	# for phone, i in zip(PHONES, range(len(PHONES))):
	for i, phone in enumerate(phones):
	    VARIABLE[phone] = tkinter.IntVar()
	    tkinter.Checkbutton(frame, 
	    					text=phone, 
	    					variable=VARIABLE[phone],
	                        command=print_source_size).place(x=starting_x, y=starting_y)
	    starting_y += 30
	    if starting_y >= 201:
	        starting_x += 150
	        starting_y = 30


def source(frame):
	source_label = tkinter.Label(frame, 
								 text="Source", 
								 fg="red", 
								 font=('Arial', 15, 'bold'))
	source_label.place(x=15, y=5)
	init_phone(frame)



def destination(frame):
	destination_label = tkinter.Label(frame,
									  text="Destination", 
									  fg="red", 
									  font=('Arial', 15, 'bold'))
	destination_label.place(x=10, y=4)

	btn_browse = tkinter.Button(frame, 
								text = "Browse", 
								command = browse)
	btn_browse.place(x = 30, y = 35)

	folder_path = browse()
	browse_path = tkinter.Label(frame, 
								text = folder_path).place(x = 30, y = 65)


def options(frame):
	option_label = tkinter.Label(frame, 
								text="Options", 
								fg="red", 
								font=('Arial', 15, 'bold')).place( x = 10, y = 10)

	var_delete = tkinter.BooleanVar()
	var_convert = tkinter.BooleanVar()

	tkinter.Checkbutton(frame, 
						text="Delete after copy", 
						variable=var_delete).place( x = 30, y = 40)
	tkinter.Checkbutton(frame, 
						text="Convert to 480 after copy", 
						variable = var_convert).place( x = 30, y = 60)

	btn_go = tkinter.Button(frame,
							text="Go", 
							bg='green',
	                    	fg='white', 
	                    	width=10, 
	                    	command=lambda: go(is_delete=var_delete.get(), is_update=var_convert.get(), destination = DESTINATION))
	btn_go.place(relx=0.5, 
				 rely=0.4, 
				 anchor= tkinter.CENTER)

	tkinter.Label(frame, 
				  text="total size: ").place(x=30, y=150)

def main():
	source(source_frame)
	destination(destination_frame)
	options(option_frame)
main()

screen.mainloop()
