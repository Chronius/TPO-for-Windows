import serial
import serial.tools.list_ports

import time
import threading, subprocess

filename = 'resources\\text.bin' #use double reverse backslash for win_cmd
filename2 = 'resources\\text_copy.bin'

state = threading.Event()

def testTxRx(Tx, Rx, baudrate):
    global Tx1, Rx1, Thread2, state

    Tx1 = serial.Serial(Tx, baudrate)
    Rx1 = serial.Serial(Rx, baudrate)

    Thread2 = True
    state.clear()

    t1 = threading.Thread(target=FromRS)
    t2 = threading.Thread(target=ToRS)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    Tx1.close()
    Rx1.close()
    print("end test")

#Thread 1
def FromRS():
    print("Start listen port")
    global state, Thread2

    with open(filename2, 'wb') as f2:   #Recieved file
        while Thread2 is True:
            if Rx1.inWaiting():
                byte = Rx1.read(Rx1.inWaiting())
                print("rx: ", byte)
                f2.write(byte)    #read() - read one byte
    f2.close()

#Thread 2
def ToRS():
    print("Start send data to port")
    global Thread2

    with open(filename, 'rb') as f: # Transmmit file
        for line in f:
            print("tx: ",line)
            Tx1.write(line)

    f.close()
    time.sleep(1)
    Thread2 = False

def start_process(command, ignore = False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not ignore:
            if (p.wait()):
                    print(command," complited with an error!")
                    exit(1)
    res = [x.decode("CP866") for x in p.stdout.readlines()] #correct output on windwos
    return  res

def main():
    print("/--------------------------------------------")
    print("Run test RS232")

    BAUDRATE = 115200

    ports = list(serial.tools.list_ports.comports())
    port_list = []

    for p in ports:
        port_list.append(p.device)

    print(port_list)
    print(port_list[1], port_list[2])
    testTxRx(port_list[1], port_list[2], BAUDRATE)
    print("switch Tx Rx")
    testTxRx(port_list[2], port_list[1], BAUDRATE)  # switch Tx<->Rx

    print(start_process('FC /B ' + filename + ' ' + filename2))  # compare file1, file2

if __name__ == '__main__':
        main()