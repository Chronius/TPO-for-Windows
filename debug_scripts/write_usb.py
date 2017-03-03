import time, struct
from hw_info import hw_info


def main():

    bin_file = open('M:\\test.bin', 'wb')
    start = time.time()
    size = 1024 * 1024 * 4

    #Writing
    for num in range(size):
        data = struct.pack('i', 0)
        bin_file.write(data)
    end = time.time()

    print("data size %i byte" % size, "or", round(size / 1024, 2), "KByte")
    end = round(end - start, 10)
    speed = size / end
    print(end, "s")
    print("write: ", round((speed / 1024) / 1024, 3), "Mbyte/sec")
    bin_file.close()

    #Reading
    bin_file = open('M:\\test.bin', 'rb')

    start = time.time()
    s = bin_file.read(1)
    while s:
        s = bin_file.read(4)
    end = time.time()
    end = round(end - start, 10)
    speed = size / end
    print(end, "s")
    print("read: ", round((speed / 1024) / 1024, 3), "Mbyte/sec")
    bin_file.close()

if __name__ == '__main__':
    #main()
    h = hw_info()
    a = h.disk_info() #a is [(name, model), ...] or a[i][j]

    print(a)
    print(len(a))
    #with open(a[0][0], "rb") as disk:
    #	print("open disk:", a[0][0], a[0][1])
    #	disk.read(1)
    #	print(disk.read(4))
    #with open(r"\\.\PHYSICALDRIVE1", "rb") as disk:
    #    disk.read(1)
    #    s = disk.read(4)
    #    print(s)
    