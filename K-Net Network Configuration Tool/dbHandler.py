#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create instance of base Class
Base = declarative_base()


class Deviceinfo(Base):
    __tablename__ = 'deviceinfo'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True,autoincrement=True)
    deviceType = Column(String(32))
    hostname = Column(String(32))
    ipAddress = Column(String(32))
    username = Column(String(32))
    password = Column(String(32))
    enable = Column(String(32))

# initialize database connection:
engine = create_engine(r'sqlite:///data/deviceinfo.db')
# create DBSession:
DBSession = sessionmaker(bind=engine)
# create session instance:
session = DBSession()



def creat_item(_deviceinfo_tuple):
    (_deviceType, _hostname, _ipAddress, _username, _password, _enable) = _deviceinfo_tuple
    # create new device:
    new_device = Deviceinfo(
        deviceType=_deviceType,
        hostname=_hostname,
        ipAddress=_ipAddress,
        username=_username,
        password=_password,
        enable=_enable)
    # add session:
    session.add(new_device)
    session.commit()
    session.close()

def read_item():
    deviceinfo_list = session.query(Deviceinfo).all()
    session.close()
    return deviceinfo_list

def update_item(*args):
    pass

def delete_item(_ipAddress):
    session.query(Deviceinfo).filter(Deviceinfo.ipAddress==_ipAddress).delete()
    session.commit()
    session.close()


# submit the trasaction
devices = session.query(Deviceinfo).all()
#print(type(devices[0]))

session.query(Deviceinfo).filter_by(id='1').update({'password':'password'})
session.commit()
#print(devices[3].deviceType)
# close session:
session.close()