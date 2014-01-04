#!/usr/bin/python

import dbus

def is_usb_mass_storage(device_props):
  if device_props['IdLabel'] != '' and \
        device_props['IdUsage'] == 'filesystem' and \
        device_props['DriveCanDetach']:
    return True
  else:
    return False

def get_device_props():
  bus = dbus.SystemBus()
  ud_manager_obj = bus.get_object('org.freedesktop.UDisks',
                                  '/org/freedesktop/UDisks')
  ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')

  proplist = []
  
  for device in ud_manager.EnumerateDevices():
    device_obj = bus.get_object('org.freedesktop.UDisks', device)
    device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)
    proplist.append(device_props.GetAll('org.freedesktop.UDisks.Device'))

  return proplist
    
for device_props in get_device_props():
  print '----------'
  print device_props['DeviceFile']
  if is_usb_mass_storage(device_props):
    print 'It\'s a usb mass storage device'
  else:
    print 'It\'s not'

