import serial
import serial.tools.list_ports

import time, sys
import threading, subprocess
import os

filename = 'resources\\data512K.bin' #use double reverse backslash for win_cmd
filename2 = 'resources\\data512K_copy.bin'

state = threading.Event()

file_size=os.path.getsize(filename)

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


def FromRS():
    """Thread 1"""
    print("Start listen port")
    global state, Thread2

    with open(filename2, 'wb') as f2:   #Recieved file
        byte_sum = 0
        per = 0
        while Thread2 is True:
            if Rx1.inWaiting():
                #byte = Rx1.read(Rx1.inWaiting())
                byte = Rx1.read(1024*10)
                byte_sum += len(byte)
                f2.write(byte)
                if int(((byte_sum*1.0)/file_size)*100/10) > int(per/10):
                    per = int(((byte_sum*1.0)/file_size)*100)
                    print("Rx:",per, "%")
                    sys.stdout.flush()
                    #read() - read one byte
    f2.close()


def ToRS():
    """Thread 2"""
    print("Start send data to port")
    global Thread2
    byte_sum = 0
    per = 0
    i = 0
    printProgressBar(0, 100, prefix='Progress:', suffix='Complete', length=50)
    with open(filename, 'rb') as f: # Transmmit file
        for line in f:
            #print("tx: ",line)
            i += Tx1.write(line)
            byte_sum += len(line)
            if int(((byte_sum*1.0)/file_size)*100/10) > int(per/10):
                per = int(((byte_sum*1.0)/file_size)*100)
                #print("Tx:",per, "%")
            printProgressBar(i, file_size, prefix='Progress:', suffix='Complete', length=50)
            sys.stdout.flush()
    f.close()
    print("file size:",file_size)
    time.sleep(2)
    #while Rx1.inWaiting():
    #    time.sleep(1)
    Thread2 = False

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    fill = '|'
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end = "\r")
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total:
        print()

def compare_size(file1, file2):
	return ((os.path.getsize(file1) - os.path.getsize(file2))/os.path.getsize(file1))*100

def start_process(command, ignore = False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    [print(x.decode("CP866").strip()) for x in p.stdout.readlines()]
    return p.wait()


def main():

    print("Run test RS232")

    ports = list(serial.tools.list_ports.comports())
    port_list = []
    
    for p in ports:
        if p and "КВ Последовательный порт" in p.description:
            port_list.append(p.device)

    print(port_list)
    sys.stdout.flush()
    
    err = 0
    try:
        for BAUDRATE in [115200, 460800, 921600]:
            print("BAUDRATE:", BAUDRATE, port_list[0],"->", port_list[3])
            sys.stdout.flush()
            testTxRx(port_list[0], port_list[3], BAUDRATE)
            cmp = compare_size(filename, filename2);
            err += cmp
            print("err:",cmp)
            print("BAUDRATE:", BAUDRATE, port_list[2],"->", port_list[1])
            sys.stdout.flush()
            testTxRx(port_list[2], port_list[1], BAUDRATE)
            cmp = compare_size(filename, filename2);            
            err += cmp
            print("err:",cmp)

        #if cmp == 0:
        #start_process('FC /B ' + filename + ' ' + filename2)  # compare file1, file2

    except serial.serialutil.SerialException:
        print("Device is busy")
        sys.stdout.flush()
        
    except serial.serialutil.SerialException:
        print("Device is busy")
        sys.stdout.flush()
        exit(1)
    except:
        print("\ncheck port list and try again")
        sys.stdout.flush()
        exit(1)
    finally:
        if err > 0:
            exit(1)

if __name__ == '__main__':
        main()
