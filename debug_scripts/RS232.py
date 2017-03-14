import serial
import serial.tools.list_ports

import time, sys
import threading, subprocess

filename = 'resources\\text.bin' #use double reverse backslash for win_cmd
filename2 = 'resources\\text_copy.bin'

state = threading.Event()


def testTxRx(Tx, Rx, baudrate):
    global Tx1, Rx1, Thread2, state

    Tx1 = serial.Serial(Tx, baudrate, timeout=1)
    Rx1 = serial.Serial(Rx, baudrate, timeout=1)

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


def FromRS():
    """Thread 1"""
    print("Start listen port")
    global state, Thread2

    with open(filename2, 'wb') as f2:   #Recieved file
        while Thread2 is True:
            if Rx1.inWaiting():
                byte = Rx1.read(Rx1.inWaiting())
                print("rx: ", byte)
                sys.stdout.flush()
                f2.write(byte)    #read() - read one byte
    f2.close()


def ToRS():
    """Thread 2"""
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
    [print(x.decode("CP866").strip()) for x in p.stdout.readlines()]
    return p.wait()


def main():

    print("Run test RS232")

    BAUDRATE = 115200

    ports = list(serial.tools.list_ports.comports())
    port_list = []
    
    for p in ports:
        if p and "КВ Последовательный порт" in p.description:
            port_list.append(p.device)


    #testTxRx(port_list[1], port_list[2], BAUDRATE)
    try:
        print(port_list)
        print(port_list[2], port_list[1])
        sys.stdout.flush()
        #testTxRx(port_list[1], port_list[2], BAUDRATE)
        print("switch Tx Rx")
        #testTxRx(port_list[3], port_list[2], BAUDRATE)  # switch Tx<->Rx

        if start_process('FC /B ' + filename + ' ' + filename2) == 1:  # compare file1, file2
            exit(1)
        else:
            exit(0)
    except serial.serialutil.SerialException:
        print("Device is busy")
        sys.stdout.flush()
        exit(1)
    except:
        print("\ncheck port list and try again")
        sys.stdout.flush()
        exit(1)

if __name__ == '__main__':
        main()