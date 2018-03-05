#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from tkinter import *
from tkinter.scrolledtext import *



class eventLog(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        super(eventLog, self).__init__(master=None, cnf={}, **kw)
        self.eventLog_scrolledText = ScrolledText(self, state='disabled', height=12)
        self.eventLog_layout()

    def eventLog_layout(self):
        eventLog_label = Label(self, text='Events Log：', borderwidth=2, relief=SOLID, anchor='w')

        eventLog_label.grid(row=0, columnspan=2, sticky='we')
        self.eventLog_scrolledText.grid(row=1, columnspan=2, sticky='we')

    def logging(self, _ipAddress,  msg=''):
        _formatMsg = '>>>>  Time:  [ ' + time.ctime() + ' ] ' + ' IP Address: [ ' + _ipAddress + ' ]  Info : \n[' + msg + ']\n\n'
        self.eventLog_scrolledText.configure(state='normal')
        self.eventLog_scrolledText.insert(END, _formatMsg)
        self.eventLog_scrolledText.configure(state='disabled')
        self.eventLog_scrolledText.update_idletasks()
