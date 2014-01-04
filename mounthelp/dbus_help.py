#!/usr/bin/python

#!/usr/bin/python

"""
dbus_help.py

Provides functions to help locate usb mass storage devices using dbus
"""

import dbus


def is_usb_mass_storage(device_props):
  # Returns whether the given dictionary of device properties is a usb mass
  # storage device or not

  if device_props['IdLabel'] != '' and \
        device_props['IdUsage'] == 'filesystem' and \
        device_props['DriveCanDetach']:
    return True
  else:
    return False

def get_device_props():
  # Returns a dict containing the properties of all udisk devices found by dbus

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

def get_usb_mass_storage_device_props():
  # Returns a list containing the properties of connected usb mass storage
  # devices

  props = get_device_props()
  usbprops = []

  for prop in props:
    if is_usb_mass_storage(prop):
      usbprops.append(prop)

  return usbprops
