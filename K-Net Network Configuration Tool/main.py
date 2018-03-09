#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = "Shawn Song"
__copyright__ = "Copyright 2018"
__credits__ = []
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Shawn Song"
__email__ = "ssc1982@gmail.com"
__status__ = "testing"

from tkinter import *
from btm_frame import eventLog
from center_left_frame import devicemgt
from center_right_notebook import telnetTab_notebook



class App(Tk):

    def __init__(self, width, height, title, icon):
        super(App, self).__init__()
        self._width = width
        self._height = height
        self._title = title
        self._icon = icon

    # define the position of the main window
    def center_window(self):
        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate position x and y coordinates
        x = (screen_width / 2) - (self._width / 2)
        y = (screen_height / 2) - (self._height / 2)

        self.geometry('%dx%d+%d+%d' % (self._width, self._height, x, y))

        #self.resizable(0,0)
        self.title(self._title)
        self.iconbitmap(self._icon)

    # layout of the main window
    def layout(self):
        # create all of the main containers
        top_frame = Frame(self, bg='light blue', height=30, pady=2, borderwidth=1, relief=SOLID)

        #add device management frame on the main window
        #center_left = Frame(self, bg='yellow', width=350, height=300, padx=2, pady=2, borderwidth=1, relief=SOLID, highlightcolor="red")
        # initialize the infor log frame
        btm_frame = eventLog(self, bg='light blue', height=250, pady=2, borderwidth=1, relief=SOLID)

        center_right_nb = telnetTab_notebook(self, btm_frame, width=630, takefocus=True)

        center_left_fr = devicemgt(self, btm_frame, center_right_nb, width=330,  bg='light blue',padx=2, pady=2, borderwidth=1, relief=SOLID, highlightcolor='red')

        btm_frame2 = Frame(self, bg='light blue', height=20, pady=2,borderwidth=1, relief=SOLID)

        #layout all of the main containers
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #
        top_frame.grid(row=0,columnspan=3, sticky="new")
        #layout of device management frame
        center_left_fr.grid(row=1,columnspan=2, sticky="nswe")
        #auto-adjust the size of the window
        center_left_fr.grid_rowconfigure(1, weight=1)
        center_left_fr.grid_columnconfigure(0, weight=1)
        #
        center_right_nb.grid(row=1, column=2, sticky="nswe")
        center_right_nb.grid_rowconfigure(1, weight=1)
        center_right_nb.grid_columnconfigure(0, weight=1)
        #
        btm_frame.grid(row=2, columnspan=3, sticky="we")
        btm_frame.grid_rowconfigure(1, weight=1)
        btm_frame.grid_columnconfigure(0, weight=1)
        #
        btm_frame2.grid(row=3, columnspan=3, sticky="swe")

        # create the widgets for the top frame


        # layout the widgets in the top frame


        # create the center widgets
        #center_left.grid_rowconfigure(0, weight=1)
        #center_left.grid_columnconfigure(1, weight=1)
        #center_right.grid_rowconfigure(0, weight=1)
        #center_right.grid_columnconfigure(1, weight=1)


    def run(self):
        self.center_window()
        self.layout()
        self.mainloop()

    def quit(self):
        self.destroy()


if __name__ == '__main__':
    app = App(992, 640, 'K-Net Network Configuration Tool', 'favicon.ico')
    app.run()
