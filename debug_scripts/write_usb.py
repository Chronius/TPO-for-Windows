import time, os, sys
sys.path.append(".\\")
from hw_info import hw_info


def copy_usb(src, dst):
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
    print("---------------------------------------------")
    print("open disk:", disk[1], "\npath",disk[0])
    print("Start test write")
    print("---------------------------------------------")
    ret_size = 0
    start = time.time()
    for i in range(4): #16Mb * N
        ret_size += copy_usb("resources/data16M.bin", disk[0])
    end = time.time()
    end = round(end - start, 10)
    speed = ret_size / end
    print(end, "s")
    print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
    speed = round((speed / 1024) / 1024, 3)
    print("write: ", speed, "Mbyte/sec")
    print("---------------------------------------------")
    if speed > 7:
        return 0
    return 1
    print("failed test with low speed, expected 7 Mb/s, result", speed)
    print("---------------------------------------------")
    sys.stdout.flush()


def raw_read(disk):
    try:
        with open(disk[0], "rb+", buffering=16 * 1024) as _disk:
            print("---------------------------------------------")
            print("\nopen disk:", disk[1], "\npath:", disk[0])
            print("Start test read")
            print("---------------------------------------------")
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
            speed = round((speed / 1024) / 1024, 3)
            print(end, "s")
            print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
            print("read: ", speed, "Mbyte/sec")
            print("---------------------------------------------")
            if speed > 7:
                return 0
            return 1
            print("failed test with low speed, expected 7 Mb/s, result", speed)
            print("---------------------------------------------")
            sys.stdout.flush()
    except:
        print("failed open disk")
        return 1
    finally:
        sys.stdout.flush()


def read_sec(disk):
    with open(disk[0], "rb") as _disk:
        print("\nopen disk:", disk[0], disk[1])
        print("Start test read\n")
        #_disk.seek(1024)   #offset
        for i in range(64): #16*64 = 1Kbyte
            print(_disk.read(16))


def main():
    h = hw_info()
    a = h.flash_info()
    os.system('cls')
    # uncomment for test all disk
    # must be very accuracy!!!
    err_count = 0
    for disk in a:
        #read_sec(disk)
        err_count += raw_write(disk)
        err_count += raw_read(disk)
    if err_count:
        exit(1)
if __name__ == '__main__':
    main()
    exit(0)
