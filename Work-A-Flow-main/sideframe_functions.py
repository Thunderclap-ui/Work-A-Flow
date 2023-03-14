import customtkinter
from tkinter import *
from tkinter.ttk import Label, Button
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3
import pandas as pd
import openpyxl
from dashboard import *
from CTkMessagebox import *
from specific_slip import ssgClass



def ssg_func(self):
    if filename:
        self.new_win=Toplevel(self.app)
        self.new_obj=ssgClass(self.new_win)
    else:
        msg = CTkMessagebox(title='Error', message="File not yet uploaded", icon='cancel', option_1='Cancel',option_2='Upload')
        if msg.get()=='Upload':
            filename = filedialog.askopenfilename(initialdir="C:\\Users\\Desktop",
                                    title="Upload file...",
                                    filetypes=(("Microsoft Excel Document",".xlsx"), ("CSV Document","*.csv")))
            if filename:
                CTkMessagebox(title='Success', message='File Uploaded Successfully!!', icon='check')
            else:
                CTkMessagebox(title='Error', message="File not yet uploaded", icon='cancel', option_1='Cancel', option_2='Upload')