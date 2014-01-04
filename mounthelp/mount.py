#!/usr/bin/python

"""
pmount_help.py

Provides functions to use pmount to allow mounting/unmounting without root
"""

from subprocess import call

def mount(device, label = ''):
  # Mounts the device and returns the label the device was mounted with

  # Mount the device
  call(['pmount', device, label])

  # If we weren't given a label, it's the name of the device
  if label == '':
    if label[-1] == '/':
      return device.split('/')[-2]
    else:
      return device.split('/')[-1]

def umount(label):
  # Unmounts the given label
  call(['pumount', label])
