import time, os
from hw_info import hw_info

def copy_usb(src, dst, length = 16*1024):
    with open(src, "rb") as fsrc:
        with open(dst, "rb+", buffering=0) as fdst:
            while 1:
                buf = fsrc.read()
                if not buf:
                    break
                fdst.write(buf)
            p = fdst.tell()
    return p

def raw_write(disk):
    print("\nopen disk:", disk[1], disk[0])
    print("Start test write\n")
    ret_size = 0
    start = time.time()
    for i in range(4): #16Mb * N
        ret_size += copy_usb("resources/data16M.bin", disk[0])
    end = time.time()
    end = round(end - start, 10)
    speed = ret_size / end
    print(end, "s")
    print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
    print("write: ", round((speed / 1024) / 1024, 3), "Mbyte/sec\n")

def raw_read(disk):
    try:
        with open(disk[0], "rb+", buffering=16 * 1024) as _disk:
            print("\nopen disk:", disk[1], "\npath:", disk[0])
            print("Start test read\n")
            length = 16 * 1024
            start = time.time()
            for i in range(5000):
                buf = _disk.read(length)
                if not buf:
                    break
            ret_size = _disk.tell()
            end = time.time()
            end = round(end - start, 10)
            speed = ret_size / end
            print(end, "s")
            print("size = ", ret_size, "bytes")
            print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
            print("read: ", round((speed / 1024) / 1024, 3), "Mbyte/sec\n")
            print("Test OK")
    except:
        print("Test FAILED")

def read_sec(disk):
    with open(disk[0], "rb") as _disk:
        print("\nopen disk:", disk[0], disk[1])
        print("Start test read\n")
        #_disk.seek(1024)
        for i in range(10):
            print(_disk.read(1))

def main():
    h = hw_info()
    a = h.flash_info()
    os.system('cls')

    for disk in a:
        raw_write(disk)
        raw_read(disk)

if __name__ == '__main__':
    main()
    