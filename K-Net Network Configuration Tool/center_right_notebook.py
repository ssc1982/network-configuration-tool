#!/usr/bin/python
# -*- coding: utf-8 -*-

import napalm

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk



class telnetTab_notebook(ttk.Notebook):
    def __init__(self, btm_frame, master=None, **kw):
        super(telnetTab_notebook, self).__init__(master=None, **kw)
        self.title_list = []
        self._btm_frame = btm_frame



    def telnetTab_layout(self, _ipAddress_list):

        self.tabPage_frame = Frame(self, bg='light blue', width= 630, padx=2, pady=2, borderwidth=1, relief=SOLID, highlightcolor='red' )
        self.title = StringVar()

        self.add_tabPage(_ipAddress_list)

        tabPage_scrolledText = ScrolledText(self.tabPage_frame, width=86)
        self.filename = StringVar()
        filename_entry = Entry(self.tabPage_frame, width=85, textvariable=self.filename)
        tabPage_browseBtn = Button(self.tabPage_frame, text="Browse", command=self.load_file, width=10)
        tabPage_sendBtn = Button(self.tabPage_frame, text="Send", width=10)

        #tabPage_frame.grid(sticky='nswe')
        self.tabPage_frame.grid_rowconfigure(1, weight=1)
        self.tabPage_frame.grid_columnconfigure(0, weight=1)

        tabPage_scrolledText.grid(row=1, columnspan=2, sticky='nswe')
        tabPage_scrolledText.grid_rowconfigure(1, weight=1)
        tabPage_scrolledText.grid_columnconfigure(0, weight=1)

        filename_entry.grid(row=1, column=0, sticky='sw')
        tabPage_browseBtn.grid(row=1, column=0, sticky='se')
        tabPage_sendBtn.grid(row=1, column=1, sticky='se')


    def load_file(self):
        fname = askopenfilename(filetypes=(("Configuration files", "*.txt;*.tex"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                print(fname)
                self.filename.set(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def add_tabPage(self, _ipAddress_list):
        if len(self.tabs()) >= 1:
            if  1 == len(_ipAddress_list):
                if _ipAddress_list[0] not in self.title_list:
                    self.title_list.append(_ipAddress_list[0])
                    self.title = _ipAddress_list[0]
                    self.add(self.tabPage_frame, text=self.title)
                else:
                    showerror('Duplicate Tab', 'This device has been connected')
            else:
                _title = 'Group of %d devices: \n%s' % (len(_ipAddress_list), str(_ipAddress_list))
                print(_ipAddress_list)
                print(self.title_list)
                if _ipAddress_list not in self.title_list:
                    self.title_list.append(_ipAddress_list)
                    self.title = _title
                    self.add(self.tabPage_frame, text=self.title)
                else:
                    showerror('Duplicate Tab', 'This device has been connected')
        else:
            if  1 == len(_ipAddress_list):
                if _ipAddress_list[0] not in self.title_list:
                    self.title_list.append(_ipAddress_list[0])
                    self.title = _ipAddress_list[0]
                    self.add(self.tabPage_frame, text=self.title)
                else:
                    showerror('Duplicate Tab', 'This device has been connected')
            else:
                _title = 'Group of %d devices: \n%s' % (len(_ipAddress_list), str(_ipAddress_list))
                print(_ipAddress_list)
                print(self.title_list)
                if _ipAddress_list not in self.title_list:
                    self.title_list.append(_ipAddress_list)
                    self.title = _title
                    self.add(self.tabPage_frame, text=self.title)
                else:
                    showerror('Duplicate Tab', 'This device has been connected')