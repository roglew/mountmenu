#!/usr/bin/python

import sys
import mounthelp.dbus_help as dbh
import mounthelp.mount as mount

def _print_horline():
  print '--------------------'

def _choice_is_valid(choice, max_choice, valid_letters):
  if choice.isdigit():
    if int(choice) < 1:
      return False
    if int(choice) > max_choice:
      return False
  else:
    if choice == '':
      return False

    if choice.lower() not in valid_letters:
      return False

  return True

running = True
while running:
  usb_devs = dbh.get_usb_mass_storage_device_props()

  if len(usb_devs) == 0:
    print 'No connected USB devices found'
    sys.exit(0)

  _print_horline()
  print "Connected usb devices:"
  cur_choice = 1
  for dev in usb_devs:
    if dev['DeviceIsMounted']:
      mounted_str = 'Mounted'
    else:
      mounted_str = 'Not Mounted'
    print '%d) %s (%s)' % (cur_choice, dev['IdLabel'], mounted_str)
    cur_choice += 1

  _print_horline()
  print '# - mount/unmount choice, r - refresh, q - quit'

  valid_letters = ['r', 'q']
  choice = raw_input('> ')
  while not _choice_is_valid(choice, cur_choice-1, valid_letters):
    print 'Please input a valid command'
    choice = raw_input('> ')

  if choice.lower() == 'q':
    running = False
  elif choice.lower() == 'r':
    pass # Just start the loop over
  else:
    choice_num = int(choice)
    props = usb_devs[choice_num-1]
    if props['DeviceIsMounted']:
      mount.umount(props['IdLabel'])
    else:
      mount.mount(props['DeviceFile'], props['IdLabel'])
      
