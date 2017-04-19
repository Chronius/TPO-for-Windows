import time, sys, os, subprocess
import multiprocessing as mp

sys.path.append(".\\")
from hw_info import hw_info

MAX_SPEED = 80

def raw_read(disk):
    print("==========================================")
    with open(disk[0], "rb+", buffering=16*1024) as _disk:
        print("\nopen disk:", disk[1])
        print("Start test read\n")
        length = 16*1024
        start = time.time()
        for i in range(100000):
            buf = _disk.read(length)
            if not buf:
                break
        ret_size = _disk.tell()
        end = time.time()
        end = round(end - start, 10)
        speed = ret_size / end
        print("Time passed", round(end, 3), "s")
        print("data size %i Mbyte" % ((ret_size / 1024) / 1024))
        print("read: ", round((speed / 1024) / 1024, 3), "Mbyte/sec\n")
        speed = round((speed / 1024) / 1024, 3)
        if speed <= MAX_SPEED:
            print("failed with: low speed")
            return 1
        print("SUCCESS")
        sys.stdout.flush()


def read_sec(disk):
    with open(disk[0], "rb") as _disk:
        print("\nopen disk:", disk[0], disk[1])
        print("Start test read\n")
        _disk.read(1)
        _disk.seek(1024)
        for i in range(1):
            print(_disk.read(10))

def foo(disk):
    count_err = 0
    with subprocess.Popen("resources\\HDD_Test.exe " + disk[0] + " 1000",
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
            for line in process.stdout:
                out = line.decode('CP866').strip()
                print(out)
                if "Speed" in out:
                    speed = out.split(" ")[2]
                    if float(speed) <= MAX_SPEED:
                        print("\nfailed with: low speed")
                        count_err += 1
                sys.stdout.flush()
            if process.wait() == 0:
                count_err += 1
    return count_err

def main():
    h = hw_info()
    a = h.hard_info() #a is [(name, model), ...] or a[i][j]
    sys.stdout.flush()
    os.system('cls')
    count_err = 0
    #uncomment for test all disk
    #must be very accuracy!!!
    p = mp.Pool()
    res = p.map(raw_read, a)
    for i in range(len(res)):
        if res[i] == 1:
            count_err += i
            print("FAILED", a[i][1], "Disk #", i)
    res = p.map(foo, a)
    for i in range(len(res)):
        if res[i] == 1:
            count_err += i
            print("FAILED", a[i][1], "Disk #", i)
    if count_err != 0:
        exit(1)

if __name__ == '__main__':
    main()
    sys.stdout.flush()
    exit(0)