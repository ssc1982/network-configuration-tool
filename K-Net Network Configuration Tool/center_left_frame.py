#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import threading

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from dbHandler import creat_item, read_item, delete_item, update_item
from popupwindow import deviceinfoInputDialog


class devicemgt(Frame):

    def __init__(self, parent, btm_frame, _center_right_nb, master=None, cnf={}, **kw):
        super(devicemgt, self).__init__(master=None, cnf={}, **kw, )
        self.tree = ttk.Treeview(self, height=18)
        self._btm_frame = btm_frame
        self._center_right_nb = _center_right_nb
        self.device_layout()

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

        # refresh the layout and recontruct the tree
        self.refresh_layout()

        # add scrollbar on the right side of center_left frame
        scrollbar = Scrollbar(self, width=20, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        # add button group on the center_left frame
        add_btn = Button(self, text='Add', command=self.add_device)
        edit_btn = Button(self, text='Edit', command=self.edit_device)
        delete_btn = Button(self, text='Delete', command=self.delete_device)
        ping_btn = Button(self, text='Ping', command=lambda : self.thread_task(self.ping_device))
        tracert_btn = Button(self, text='Traceroute', command=lambda : self.thread_task(self.tracert_device))
        telnet_btn = Button(self, text='Telnet', command=lambda : self.thread_task(self.telnet_device))
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

    #check if the object is empty
    def is_empty(self, obj):
        if obj:
            return True
        else:
            return False

    def show_warnning(func):
        def wrapper(self):
            if self.is_empty(self.tree.selection()):
                func(self)
            else:
                showwarning('Warning', 'Please at least select one device !')
                return
        return wrapper

    def add_device(self):
        deviceinfo_inputDialog = deviceinfoInputDialog(())
        self.wait_window(deviceinfo_inputDialog)
        if deviceinfo_inputDialog.deviceinfo_tuple is None:
            return
        elif not 'router' == deviceinfo_inputDialog.deviceinfo_tuple[0] and \
                not 'switch' == deviceinfo_inputDialog.deviceinfo_tuple[0]:
            print(not 'router' == deviceinfo_inputDialog.deviceinfo_tuple[0])
            #print(not 'switch' == deviceinfo_inputDialog.deviceinfo_tuple[0])
            return
        creat_item(deviceinfo_inputDialog.deviceinfo_tuple)
        self.refresh_layout()
        self._btm_frame.logging(deviceinfo_inputDialog.deviceinfo_tuple[2],
                                 'A new device has been added to the system !')

    @show_warnning
    def edit_device(self):
        if len(self.tree.selection()) > 1 :
            showerror('More Items', 'You can\'t edit more than one device once !')
            return
        _deviceinfo_dict = self.tree.item(self.tree.selection())
        deviceinfo_inputDialog = deviceinfoInputDialog(self.tree.parent(self.tree.selection()), _deviceinfo_dict)
        self.wait_window(deviceinfo_inputDialog)
        if deviceinfo_inputDialog.deviceinfo_tuple is None:
            return
        update_item(deviceinfo_inputDialog.deviceinfo_tuple)
        self.refresh_layout()
        self._btm_frame.logging(deviceinfo_inputDialog.deviceinfo_tuple[2],
                                 'An update has been made to this device !')

    @show_warnning
    def delete_device(self):
        rs = askokcancel('Danger Action', 'Are you sure you want to delete the device ?')
        if rs:
            for iid in self.tree.selection():
                _devices_dict = self.tree.item(iid)
                if 0 == len(_devices_dict['values']):
                    showerror('Worng Item', 'This is not a device !')
                    return
                delete_item(_devices_dict['values'][0])
        self.refresh_layout()
        self._btm_frame.logging(_devices_dict['values'][0], 'This device has been removed from the system !')

    def refresh_layout(self):
        self.tree.delete(*self.tree.get_children())
        _deviceinfo_list = read_item()
        for _deviceinfo_tuple in _deviceinfo_list:
            self.tree_constructor(_deviceinfo_tuple)

    def thread_task(self, func):
        _thread = threading.Thread(target=func)
        _thread.start()
        #_thread.join()

    def selection_item(func):
        def wrapper(self):
            for iid in self.tree.selection():
                _devices_dict = self.tree.item(iid)
                if 0 == len(_devices_dict['values']):
                    showerror('Worng Item', 'This is not a device !')
                    return
                func(self)
        return wrapper

    @show_warnning
    def ping_device(self):
        for iid in self.tree.selection():
            _devices_dict = self.tree.item(iid)
            if 0 == len(_devices_dict['values']):
                showerror('Worng Item', 'This is not a device !')
                return
            process = subprocess.Popen(['ping', '-n', '1', '-l', '1470', _devices_dict['values'][0]],
                                        stdout = subprocess.PIPE, stderr = subprocess.PIPE )
            _output, _error = process.communicate()
            self._btm_frame.logging(_devices_dict['values'][0],  _output.decode('utf-8'))
            #print(_error.decode('UTF-8'))

    @show_warnning
    def telnet_device(self):
        _ipAddress_list = []
        for iid in self.tree.selection():
            _devices_dict = self.tree.item(iid)
            if 0 == len(_devices_dict['values']):
                showerror('Worng Item', 'This is not a device !')
                return
            _ipAddress_list.append(_devices_dict['values'][0])
            print(_devices_dict)
            self._btm_frame.logging(_devices_dict['values'][0], 'Connecting to IP Address: %s '% str(_devices_dict['values'][0]))
        self._center_right_nb.telnetTab_layout(_devices_dict)


    @show_warnning
    def tracert_device(self):
        for iid in self.tree.selection():
            _devices_dict = self.tree.item(iid)
            if 0 == len(_devices_dict['values']):
                showerror('Worng Item', 'This is not a device !')
                return
            process = subprocess.Popen(['tracert', '-d', _devices_dict['values'][0]],
                                        stdout = subprocess.PIPE, stderr = subprocess.PIPE )
            _output, _error = process.communicate()
            print(_output.decode('utf-8'))
            self._btm_frame.logging(_devices_dict['values'][0], _output.decode('utf-8'))
            #print(_error.decode('UTF-8'))
