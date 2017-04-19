import subprocess, sys, os, time
sys.path.append(".\\")
from hw_info import hw_info

dir_iperf = "resources\\soft\\iperf2\\"
#dir_iperf = "C:\develop\TPO_Debug\\resources\\soft\\iperf\\"
#target_ip = " 192.168.202.181 "
target_ip = " 10.0.0.2 "
cmd = "iperf.exe -c"+target_ip+"-t 1 -P4"
#cmd = "iperf.exe -c localhost -t 1 -P4"


def eth_enable(index):
    err = 0    
    with subprocess.Popen("wmic path win32_networkadapter\
    where index="+ str(index) +" call enable", stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        if proc.wait() == 0:
            print(str(index) + " success enable")
            sys.stdout.flush()
            return 0
        else:
            print(str(index) + " enable failed")
            sys.stdout.flush()
            return 1

def eth_disable(index):
    err = 0    
    with subprocess.Popen("wmic path win32_networkadapter\
    where index="+ str(index) +" call disable", stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        if proc.wait() == 0:
            print(str(index) + " success disable")
            sys.stdout.flush()
            return 0
        else:
            print(str(index) + " disable failed")
            sys.stdout.flush()
            return 1

def eth_disable_all(eth_list):
    err = 0
    for i in eth_list:
        with subprocess.Popen("wmic path win32_networkadapter\
        where index="+ str(i[0]) +" call disable", stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
            if proc.wait() == 0:
                print(i[2] + " success disable")
            else:
                err += 1
    if err:
        print(i[2] + " failed disable")
        sys.stdout.flush()
        return 1
    sys.stdout.flush()
    return 0

def iperf_run(name):
    MAX_SPEED = 800
    str_cmd = dir_iperf + cmd
    res_list = []
    print("\nrun iperf start on " + str(name))
    try:
        with subprocess.Popen(str_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1) as f:
            for x in f.stdout.readlines():
                print(x.decode("CP1251").strip())
                if b"SUM" in x[1:5]:
                    # iperf 3 
                    # res_list.append(float(x[38:43]))
                    #iperf 2
                    res_list.append(float(x[34:38]))
    except:
        print("Run iperf and try again")
        return 1
    sys.stdout.flush()
    try:
        average = sum(res_list) / len(res_list)
        for res in res_list:
            print("sum speed =", res, "Mbits/sec")
        if average < MAX_SPEED:
            print("Speed is less than expected")
            return 1
        else:
            print("\nAverage speed = ", round(average, 3) , "Mbits/sec")
    except:
        return 1
    finally:
        sys.stdout.flush()
    return 0

def main():
    err_count = 0
    hw = hw_info()
    eth_list = hw.eth_info()
    os.system("cls")

    for i in eth_list:
        err_count += eth_disable_all(eth_list)
        err_count += eth_enable(i[0])
        if os.system("ping"+target_ip + "-n 15") == 0:
            err_count += iperf_run(i[2])
        else:
            print("PING: connect failed")
            err_count += 1
        #err_count += eth_disable_all(eth_list)

    if err_count != 0:
        exit(1)

if __name__ == '__main__':
        main()