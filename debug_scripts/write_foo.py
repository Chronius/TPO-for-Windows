import time, wmi
from shutil import copyfile

def raw_read(disk):
    with open(disk[0], "rb") as _disk:
        print("\nopen disk:", disk[0], disk[1])
        print("Start test read\n")
        _disk.read(1)
        start = time.time()
        for i in range(10000):
            _disk.read(256)
        end = time.time()
        end = round(end - start, 10)
        speed = 10000*256 / end
        print(end, "s")
        print("read: ", round((speed / 1024) / 1024, 3), "Mbyte/sec\n")

def copy_usb(src, dst, length = 16*1024):
    with open(src, "rb") as fsrc:
        with open(dst[0], "rb+") as fdst:
            while 1:
                buf = fsrc.read(length)
                if not buf:
                    break
                fdst.write(buf)

def main():   
    w = wmi.WMI()
    usb_list = [] #usb_list is [(name, model), ...] or a[i][j]
    for disk in w.Win32_DiskDrive():
        if "SanDisk Ultra" in disk.Model or "Virtual Disk" in disk.Model:
            print("break",disk.Model)
            continue
        elif "Removable Media" in disk.MediaType:
            usb_list.append((disk.name, disk.Model))
    if usb_list:
        print(usb_list[0][0])

    #not uncomment!!!
    """
    with open(r"\\.\PHYSICALDRIVE1", "rb") as disk:
        disk.read(1)
        s = disk.read(4)
    start = time.time()
    for i in range(6): #16Mb * 6 = 96Mb
        copy_usb("resources/data16M.bin", usb_list[0])
    speed = ((i+1)*16)/ (time.time() - start)
    print(time.time() - start)
    print("write:", speed, "Mb/sec")
    """
    #copyfile("resources/data1M.bin", r"\\.\PHYSICALDRIVE1")

    #copyfile("resources/data1M.bin", r"\\.\PHYSICALDRIVE5")

    #raw_read(a[0])
    
if __name__ == '__main__':
    main()
    