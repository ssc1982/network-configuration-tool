#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from dbHandler import creat_item, read_item, delete_item
from popupwindow import deviceinfoInputDialog


class devicemgt(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master=None, cnf={}, **kw)
        self.tree = ttk.Treeview(self, height=18)

    def device_layout(self):

        # define the tree columns and
        self.tree['columns'] = ('#1', '#2', '#3', '#4')
        self.tree.column('#0', width=70)
        self.tree.column('#1', width=66)
        self.tree.column('#2', width=66)
        self.tree.column('#3', width=66)
        self.tree.column('#4', width=66)
        # define the heading name for each column
        self.tree.heading('#0', text='Hostname')
        self.tree.heading('#1', text='IP Address')
        self.tree.heading('#2', text='Username')
        self.tree.heading('#3', text='Password')
        self.tree.heading('#4', text='Enable')

        self.view_device()

        # add scrollbar on the right side of center_left frame
        scrollbar = Scrollbar(self, width=20, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # add button group on the center_left frame
        add_btn = Button(self, text='Add', command=self.add_device)
        edit_btn = Button(self, text='Edit', command=self.edit_device)
        delete_btn = Button(self, text='Delete', command=self.delete_device)
        ping_btn = Button(self, text='Ping', command=self.ping_device)
        tracert_btn = Button(self, text='Traceroute', command=self.tracert_device)
        telnet_btn = Button(self, text='Telnet', command=self.telnet_device)
        # define grid layout of tree, scrollbar and buttons
        self.tree.grid(row=1, columnspan=6, sticky="nswe")
        scrollbar.grid(row=1, column=6, sticky='nsw')
        add_btn.grid(row=2, column=0, sticky='e')
        edit_btn.grid(row=2, column=1, sticky='we')
        delete_btn.grid(row=2, column=2, sticky='we')
        ping_btn.grid(row=2, column=3, sticky='we')
        tracert_btn.grid(row=2, column=4, sticky='we')
        telnet_btn.grid(row=2, column=5, sticky='we')

    def tree_constructor(self, _deviceinfo_tuple):
        if 'router' == _deviceinfo_tuple.deviceType:
            if not self.tree.exists('router'):
                global node1
                node1 = self.tree.insert('', 0, 'router', text=_deviceinfo_tuple.deviceType)
                self.tree.item('router', open=True)
                self.tree.insert(node1, 1, text=_deviceinfo_tuple.hostname, values=(_deviceinfo_tuple.ipAddress,
                                                                                    _deviceinfo_tuple.username,
                                                                                    _deviceinfo_tuple.password,
                                                                                    _deviceinfo_tuple.enable))
            else:
                self.tree.insert(node1, 1, text=_deviceinfo_tuple.hostname, values=(_deviceinfo_tuple.ipAddress,
                                                                                    _deviceinfo_tuple.username,
                                                                                    _deviceinfo_tuple.password,
                                                                                    _deviceinfo_tuple.enable))
        elif 'switch' == _deviceinfo_tuple.deviceType:
            ##alternatively:
            if not self.tree.exists('switch'):
                global node2
                node2 = self.tree.insert("", 0, 'switch', text=_deviceinfo_tuple.deviceType)
                self.tree.item('switch', open=True)
                self.tree.insert(node2, 1, text=_deviceinfo_tuple.hostname, values=(_deviceinfo_tuple.ipAddress,
                                                                                    _deviceinfo_tuple.username,
                                                                                    _deviceinfo_tuple.password,
                                                                                    _deviceinfo_tuple.enable))
            else:
                self.tree.insert(node2, 1, text=_deviceinfo_tuple.hostname, values=(_deviceinfo_tuple.ipAddress,
                                                                                    _deviceinfo_tuple.username,
                                                                                    _deviceinfo_tuple.password,
                                                                                    _deviceinfo_tuple.enable))

        else:
            print('wrong device type')

    def add_device(self):
        deviceinfo_inputDialog = deviceinfoInputDialog()
        self.wait_window(deviceinfo_inputDialog)
        print(deviceinfo_inputDialog.deviceinfo_tuple[0])
        if not 'router' == deviceinfo_inputDialog.deviceinfo_tuple[0] or \
                not 'switch' == deviceinfo_inputDialog.deviceinfo_tuple[0] :
            return
        creat_item(deviceinfo_inputDialog.deviceinfo_tuple)
        self.view_device()

    def edit_device(self):
        pass

    def delete_device(self):
        _devices_dict = self.tree.item(self.tree.selection())
        print(_devices_dict['values'][0])
        delete_item(str(_devices_dict['values'][0]))
        print(self.tree.item(self.tree.selection()))
        self.view_device()

    def view_device(self):
        self.tree.delete(*self.tree.get_children())
        _deviceinfo_list = read_item()
        for _deviceinfo_tuple in _deviceinfo_list:
            self.tree_constructor(_deviceinfo_tuple)

    def ping_device(self):
        pass

    def telnet_device(self):
        pass

    def tracert_device(self):
        pass

    def connect_device(self):
        pass
