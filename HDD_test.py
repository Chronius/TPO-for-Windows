import subprocess
import os

dir_stressdisk = "resources\soft\stressdisk\\"

cmd = "stressdisk.exe run "

disks_to_check = []


import string
from ctypes import windll

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives

if __name__ == '__main__':

    err_count = 0
    elapsed_t = None
    print(get_drives())
    str = dir_stressdisk + cmd + "H:"

    with subprocess.Popen(str, stderr=subprocess.PIPE) as f:
        while f.poll() is None:
            x = f.stderr.readline()
            #print(x)
            if b"Bytes read" in x or b"Reading file" in x \
                    or b"Writing file" in x or b"Bytes written" in x:
                print(x)
            if b"Errors" in x:
                err_count = int(x[24:25])
            if b"Elapsed" in x:
                elapsed_t = x

    if not err_count:
        print("Test OK")
    else:
        print("Test failed\nErrors :", err_count, elapsed_t)

