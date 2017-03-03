import time, sys
from hw_info import hw_info


def copy_usb(src, dst, length = 16*1024):
    with open(src, "rb") as fsrc:
        with open(dst, "rb+") as fdst:
            while 1:
                buf = fsrc.read(length)
                if not buf:
                    break
                fdst.write(buf)


def raw_write(disk):
    print("\nopen disk:", disk[1], disk[0])
    print("Start test write\n")
    start = time.time()
    for i in range(6): #16Mb * 6 = 96Mb
        copy_usb("resources/data16M.bin", disk[0])
    end = time.time()
    end = round(end - start, 10)
    size = (i+1)*16
    speed = size / end
    print(end, "s")
    print("data size %i Mbyte" % size)
    print("write:", speed, "Mbyte/sec\n")


def raw_read(disk):
    with open(disk[0], "rb+") as _disk:
        print("\nopen disk:", disk[1], disk[0])
        print("Start test read\n")
        _disk.read(1)
        length = 1*1024
        ret_size = 0
        start = time.time()
        for i in range(100000):
            buf = _disk.read(length)
            if not buf:
                break
            ret_size += sys.getsizeof(buf)
            
        end = time.time()
        end = round(end - start, 10)
        speed = ret_size / end
        print(end, "s")
        print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
        print("read: ", round((speed / 1024) / 1024, 3), "Mbyte/sec\n")

def read_sec(disk):
    with open(disk[0], "rb") as _disk:
        print("\nopen disk:", disk[0], disk[1])
        print("Start test read\n")
        _disk.read(1)
        _disk.seek(1024)
        for i in range(1):
            print(_disk.read(10))

def main():
    h = hw_info()
    a = h.disk_info() #a is [(name, model), ...] or a[i][j]

    #raw_write(a[0])
    #raw_read(a[0])

    #uncomment for test all disk
    #must be very accuracy!!!
    #for disk in a:
    #    raw_read(disk)

if __name__ == '__main__':
    main()