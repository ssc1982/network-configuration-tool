#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *


class deviceinfoInputDialog(Toplevel):

  def __init__(self, *_deviceinfo_tuple):
    super(deviceinfoInputDialog, self).__init__()
    self.title('Deviceinfo Input')
    #self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.geometry('300x180+300+200')
    self.resizable(0, 0)
    self.inputDialog_layout(_deviceinfo_tuple)
    self.protocol("WM_DELETE_WINDOW", self.cancel)

  def inputDialog_layout(self, _deviceinfo_tuple):

    #define labels and entries for all the components
    deviceType_label = Label(self, text='Deivce Type：', width=10, borderwidth=2, relief=SOLID)
    choices = {'router', 'switch'}
    self.deviceType = StringVar()

    deviceType_optionMenu = OptionMenu(self, self.deviceType, *choices)

    hostname_label = Label(self, text='Hostname：', width=10,  borderwidth=2, relief=SOLID)
    self.hostname = StringVar()
    hostname_entry = Entry(self, textvariable=self.hostname, width=20)

    ipAddress_label = Label(self, text='IP Address：', width=10,  borderwidth=2, relief=SOLID)
    self.ipAddresss = StringVar()
    ipAddress_entry = Entry(self, textvariable=self.ipAddresss, width=20)

    username_label = Label(self, text='Username：', width=10,  borderwidth=2, relief=SOLID)
    self.username = StringVar()
    username_entry = Entry(self, textvariable=self.username, width=20)

    password_label = Label(self, text='Password：', width=10,  borderwidth=2, relief=SOLID)
    self.password = StringVar()
    password_entry = Entry(self, textvariable=self.password, width=20)

    enable_label = Label(self, text='Enable：', width=10,  borderwidth=2, relief=SOLID)
    self.enable = StringVar()
    enable_entry = Entry(self, textvariable=self.enable, width=20)

    if all(_deviceinfo_tuple):
      _deviceType, _deviceinfo_dict = _deviceinfo_tuple
      self.deviceType.set(_deviceType)
      self.hostname.set(_deviceinfo_dict['text'])
      self.ipAddresss.set(_deviceinfo_dict['values'][0])
      self.username.set(_deviceinfo_dict['values'][1])
      self.password.set(_deviceinfo_dict['values'][2])
      self.enable.set(_deviceinfo_dict['values'][3])
      #device type and IP Address are not allowed to edit
      deviceType_optionMenu.config(state=DISABLED)
      ipAddress_entry.config(state=DISABLED)

    ok_btn = Button(self, text='OK', command=self.ok)
    cancel_btn = Button(self, text='Cancel', command=self.cancel)

    #define grid layout of all the components
    deviceType_label.grid(row=0, column=0, sticky='we')
    deviceType_optionMenu.grid(row=0, column=1, sticky='we')
    hostname_label.grid(row=1, column=0, sticky='we')
    hostname_entry.grid(row=1, column=1, sticky='we')
    ipAddress_label.grid(row=2, column=0, sticky='we')
    ipAddress_entry.grid(row=2, column=1, sticky='we')
    username_label.grid(row=3, column=0, sticky='we')
    username_entry.grid(row=3, column=1, sticky='we')
    password_label.grid(row=4, column=0, sticky='we')
    password_entry.grid(row=4, column=1, sticky='we')
    enable_label.grid(row=5, column=0, sticky='we')
    enable_entry.grid(row=5, column=1, sticky='we')
    ok_btn.grid(row=6, column=0, sticky='swe')
    cancel_btn.grid(row=6, column=1, sticky='swe')

  def ok(self, deviceType_entry=None):
    self.deviceinfo_tuple = (self.deviceType.get(),
                             self.hostname.get(),
                             self.ipAddresss.get(),
                             self.username.get(),
                             self.password.get(),
                             self.enable.get() )
    self.destroy()

  def cancel(self):
    self.deviceinfo_tuple = None
    self.destroy()

if __name__ == '__main__':
    diid = deviceinfoInputDialog()
    diid.inputDialog_layout()
    diid.mainloop()


