#!/usr/bin/python2
import usb.core
import usb.util

def find_usb_devices(vid, pid):
    return [(d.bus, d.address, d.serial_number) for d in usb.core.find(find_all = True, idVendor = vid, idProduct = pid)]

if __name__ == '__main__':
    # These are for an FTDI USB-serial chip. Replace with
    # the appropriate vid, pid for the Keysight U2000.
    vid = 0x0403
    pid = 0x6001
    for device in find_usb_devices(vid, pid):
        print "bus %d address %d: serial %s" % device
