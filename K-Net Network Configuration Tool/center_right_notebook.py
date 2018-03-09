#!/usr/bin/python
# -*- coding: utf-8 -*-

import napalm
import os

from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk



class telnetTab_notebook(ttk.Notebook):
    def __init__(self, parent, btm_frame, master=None, **kw):
        super(telnetTab_notebook, self).__init__(master=None, **kw)
        self.enable_traversal()
        self.title_list = []
        self._btm_frame = btm_frame #import bottom frame instance
        self.scrolledTextInstance_dict = {} #save scrolledTextInstance into dictionary
        self.connections_dict = {} #save connections into this dictionary


    def telnetTab_layout(self, _devices_list):

        self.tabPage_frame = Frame(self, bg='light blue', width=630, padx=2, pady=2, borderwidth=1, relief=SOLID,
                                   highlightcolor='red')
        self.tabPage_scrolledText = ScrolledText(self.tabPage_frame, width=86)

        self.filename = StringVar()
        filename_entry = Entry(self.tabPage_frame, width=85, textvariable=self.filename)
        tabPage_browseBtn = Button(self.tabPage_frame, text="Browse", command=self.load_file, width=10)
        tabPage_sendBtn = Button(self.tabPage_frame, text="Send", width=10, command=self.send_cmd)

        #tabPage_frame.grid(sticky='nswe')
        self.tabPage_frame.grid_rowconfigure(1, weight=1)
        self.tabPage_frame.grid_columnconfigure(0, weight=1)

        self.tabPage_scrolledText.grid(row=1, columnspan=2, sticky='nswe')
        self.tabPage_scrolledText.grid_rowconfigure(1, weight=1)
        self.tabPage_scrolledText.grid_columnconfigure(0, weight=1)

        filename_entry.grid(row=1, column=0, sticky='sw')
        tabPage_browseBtn.grid(row=1, column=0, sticky='se')
        tabPage_sendBtn.grid(row=1, column=1, sticky='se')

        self.add_tabPage(_devices_list)

    def add_tabPage(self, _devices_list):
        self.title = StringVar()
        _devicesinfo_list = []
        for _deviceinfo in _devices_list:
            _devicesinfo_list.append(_deviceinfo['values'][0])
        if _devicesinfo_list not in self.title_list:
            self.title_list.append(_devicesinfo_list)
            self.title = _devicesinfo_list
            self.add(self.tabPage_frame, text=self.title)
            self.select(self.tabPage_frame)

            # put the new created instance into dictionary
            self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']] = self.tabPage_scrolledText
            #connecting to each devices
            self.connect_device(_devices_list)
        else:
            showerror('Duplicate Tab', 'This device has been connected')

    def connect_device(self, _device_list):
        driver = napalm.get_network_driver('ios')
        for _devices_dict in _device_list:
            device = driver(hostname=_devices_dict['values'][0],
                            username=_devices_dict['values'][1],
                            password=_devices_dict['values'][2],
                            optional_args={'transport': 'telnet', 'secret': _devices_dict['values'][3]})

            try:
                self._btm_frame.logging(_devices_dict['values'][0],
                                        'Sending request to IP Address: %s ' % str(_devices_dict['values'][0]))
                device.open()
                self._btm_frame.logging(_devices_dict['values'][0],
                                        'Conencted to IP Address: %s ' % str(_devices_dict['values'][0]))
            except TimeoutError as e:
                self._btm_frame.logging(_devices_dict['values'][0], str(e))
                return
            except TypeError as e:
                self._btm_frame.logging(_devices_dict['values'][0], str(e))
                return
            except BaseException as e:
                self._btm_frame.logging(_devices_dict['values'][0], str(e))
                return
            finally:
                self.connections_dict[_devices_dict['values'][0]] = device

    def load_file(self):
        fname = askopenfilename(filetypes=(("Configuration files", "*.txt;*.tex"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.filename.set(fname)
                self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].delete(1.0, END)
                self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].configure(state='disabled')
                self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].update_idletasks()
            except:                     # <- naked except is a bad idea
                showerror("Open Configuration File", "Failed to read file\n'%s'" % fname)
            return
        else:
            self.filename.set('')
            self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].configure(
                state='normal')
            self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].update_idletasks()
        try:
            for i in self.tab(self.select(), "text").split(' '):
                output = self.connections_dict[i].compare_config()
                self._btm_frame.logging(i, output)
        except AttributeError as e:
            self._btm_frame.logging(i, str(e))
            return
        except BaseException as e:
            self._btm_frame.logging(i,  str(e))
            return

    def send_cmd(self):
        if self.filename.get() != '':
            rs = askokcancel('Change Notification', 'Are you sure you want to commit these changes ?')
            if rs:
                try:
                    for i in self.tab(self.select(), "text").split(' '):
                        output = self.connections_dict[i].commit_config()
                        self._btm_frame.logging(i, output)
                except AttributeError as e:
                    self._btm_frame.logging(i, str(e))
                    return
                except BaseException as e:
                    self._btm_frame.logging(i, str(e))
                    return
            else:
                self.filename.set('')
                self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].configure(
                    state='normal')
                try:
                    for i in self.tab(self.select(), "text").split(' '):
                        output = self.connections_dict[i].discard_config()
                        self._btm_frame.logging(i, output)
                except AttributeError as e:
                    self._btm_frame.logging(i, str(e))
                    return
                except BaseException as e:
                    self._btm_frame.logging(i, str(e))
                    return
        else:
            msg = self.scrolledTextInstance_dict[self.nametowidget(self.select()).children['!frame']].get(index1='1.0', index2='end-1c')
            if len(msg) == 0:
                showinfo('Telnet Panel', 'The command line can\'t empty !')
                return
            try:
                for i in self.tab(self.select(), "text").split(' '):
                    output = self.connections_dict[i].cli(msg.split('\n'))
                    self._btm_frame.logging(i, output[msg])
            except AttributeError as e:
                self._btm_frame.logging(i, str(e))
                return
            except BaseException as e:
                self._btm_frame.logging(i,  str(e))
                return