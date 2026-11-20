from pathlib import Path
import psutil
def find_usb_drivers():
    usb_drivers = []

    for usb in psutil.disk_partitions(all=False):
        if "removable" in usb.opts:
            usb_drivers.append(Path(usb.mountpoint))

    return usb_drivers[0]

print(find_usb_drivers())


