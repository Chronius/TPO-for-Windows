import wmi, subprocess, sys
from time import sleep

Drive_Type = {"Unknown" : 0, "No Root Directory" : 1, "Local Disk" : 2,
             "Network Drive" : 3, "Compact Disc" : 4, "RAM Disk" : 5}

dir_tool = "resources\\soft\\"


class hw_info():
    def __init__(self):
        self.w = wmi.WMI()
        self.list_info = [arg for arg in dir(self) if (callable(getattr(self, arg)) \
                                                and not arg.startswith('_'))]

        self.dict_info = dict((k, False) for k in self.list_info)

    #return list of tuples [(Type0, Name0), (Type1, Name1), ...]
    def hard_info(self):
        disk_list = []
        print("=======================================")
        for disk in self.w.Win32_DiskDrive():
            if "SanDisk Ultra" in disk.Model or "Virtual Disk" in disk.Model:
                continue
            if "Removable" in disk.MediaType:
                continue
            print("Name =", disk.Name)
            print("Model =", disk.Model)
            print("MediaType =", disk.MediaType)
            size = (int(disk.Size)/pow(1024,3))
            print("Size =", round(size, 2), "Gbyte")
            print("Sector size =", disk.BytesPerSector)
            print("Serial number =", disk.SerialNumber)
            print("InterfaceType =", disk.InterfaceType)
            print("---------------------------------------")
            disk_list.append((disk.Name, disk.Model))
        return disk_list

    def flash_info(self):
        disk_list = []
        print("=======================================")
        for disk in self.w.Win32_DiskDrive():
            # if "SanDisk Ultra" in disk.Model or "Virtual Disk" in disk.Model:
            #     continue
            # if "Fixed hard" in disk.MediaType:
            #     continue
            if "Fixed hard" in disk.MediaType:
                continue
            if "4C530001211008107113" in disk.SerialNumber or "Virtual Disk" in disk.Model:
                continue
            print("Name =", disk.Name)
            print("Model =", disk.Model)
            print("MediaType =", disk.MediaType)
            size = (int(disk.Size) / pow(1024, 3))
            print("Size =", round(size, 2), "Gbyte")
            print("Sector size =", disk.BytesPerSector)
            print("Serial number =", disk.SerialNumber)
            print("InterfaceType =", disk.InterfaceType)
            print("---------------------------------------")
            disk_list.append((disk.Name, disk.Model))
        return disk_list

    def com_info(self):
        print("=======================================")
        import serial
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
        # for port in self.w.Win32_SerialPort():
        #     print("Name =", port.Name)
        #     print("ProviderType =", port.ProviderType)
        #     print("MaxBaudRate =", port.MaxBaudRate)
        #     print("Status =", port.Status)
            print("---------------------------------------")

    def ram_info(self):
        print("=======================================")
        for dev in self.w.Win32_PhysicalMemory():
            print("Name =", dev.Name)
            print("Manufacturer =", dev.Manufacturer)
            size = int(dev.Capacity)/pow(1024, 3)
            print("Capacity =", size, "Gbyte")
            print("DeviceLocator =", dev.DeviceLocator)
            print("SerialNumber =", dev.SerialNumber)
            print("---------------------------------------")
        for dev in self.w.Win32_PerfFormattedData_PerfOS_Memory():
            print("Memory free =", dev.AvailableMbytes, "Mb")
            print("")

    def usb_info(self):
        print("=======================================")
        for d in self.w.Win32_USBControllerDevice():
            print(d.Dependent.Name)
            print(d.Dependent.DeviceID)
            print("---------------------------------------")

    def gpu_info(self):
        print("=======================================")
        for gpu in self.w.Win32_VideoController():
            print("Name =", gpu.Name)
            print("Hight =",gpu.CurrentVerticalResolution)
            print("Wedght =", gpu.CurrentHorizontalResolution)
            print("---------------------------------------")

    def voltage_info(self):
        volt_type = {1: "VCORE", 2: "1V8", 3: "2V5", 4: "3V3", 5: "VBAT", 6: "5V", 7: "5VSB", 8: "12V", 9: "AC"}
        sens_count = 0
        print("=======================================")
        with subprocess.Popen(dir_tool+"ktool32.exe volt GetVoltageSensorCount ",
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
            for line in process.stdout.readlines(): # b'\n'-separated lines
                if b"count" in line:                    
                    sens_count = int(line[22:26].decode('CP866'))
            for i in range(sens_count):
                with subprocess.Popen(dir_tool+"ktool32.exe volt GetVoltageSensorInfo " + str(i),
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                    for line in process.stdout.readlines():
                        if b"name" in line:                    
                            print(line.decode("CP1251").strip())
                with subprocess.Popen(dir_tool+"ktool32.exe volt GetVoltageSensorValue " + str(i),
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                    for line in process.stdout.readlines():
                        if b"value" in line:
                            sens_value = float(line[14:21])
                            sens_value /= 1000
                            print("Value = ", sens_value , "V")
                            print("---------------------------------------")

    def temp_info(self):
        temp_type = {1: "CPU", 2: "BOX", 3: "ENV", 4: "BOARD", 5: "BACKPLANE", 6: "CHIPSET", 7:"VIDEO"}
        sens_count = 0        
        print("=======================================")
        with subprocess.Popen(dir_tool+"ktool32.exe temp GetTempSensorCount ",
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
            for line in process.stdout.readlines(): # b'\n'-separated lines
                if b"count" in line:                    
                    sens_count = int(line[27:28].decode('CP866'))

            for i in range(sens_count):
                with subprocess.Popen(dir_tool+"ktool32.exe temp GetTempSensorInfo " + str(i),
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                    for line in process.stdout.readlines(): 
                        if b"name" in line:                    
                            sens_name = line.decode('CP866').strip()
                        if b"type" in line:
                            sens_type = line[6:9]
                            sens_type = int(sens_type)
                            for j in temp_type:
                                if j == sens_type:
                                    print(sens_name +" on "+ temp_type[sens_type])

                with subprocess.Popen(dir_tool+"ktool32.exe temp GetTempSensorValue " + str(i),
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, bufsize=1) as process:
                    for line in process.stdout.readlines():
                        if b"value" in line:
                            sens_value = float(line[14:21])
                            sens_value /= 1000
                            print("Temperature = ", sens_value)
                            print("---------------------------------------")

    def cpu_info(self):
        print("=======================================")
        for cpu in self.w.Win32_Processor():
            print(cpu.Name)
            print("CPU Family =", cpu.Caption)
            print("NumberOfCores =", cpu.NumberOfCores)
            print("L2CacheSize =", cpu.L2CacheSize)
            print("L3CacheSize =", cpu.L3CacheSize)
            print("CurrentClockSpeed =", cpu.CurrentClockSpeed)
            print("CPU load =", cpu.LoadPercentage, "%")
            print("---------------------------------------")

    def pci_info(self):
        print("=======================================")
        for f in self.w.Win32_PnPEntity():
            if f.DeviceID and f.Name and "PCI" in f.DeviceID \
            and not "Стандартный" in f.Name:
                print(f.Name)
                print("---------------------------------------")

    def display_info(self):
        print("=======================================")
        for d in self.w.Win32_DesktopMonitor():
            print("Name =", d.Name)
            print("Device ID =", d.DeviceID)
            print("ScreenHeight =", d.ScreenHeight)
            print("ScreenWidth =", d.ScreenWidth)
            print("---------------------------------------")

    def eth_info(self):
        #enable all adapters to see macaddress if there is
        num = 11
        ind_list = []
        print("=======================================")
        for nic in self.w.Win32_NetworkAdapterConfiguration():
            if "I210" in str(nic.Description):
                with subprocess.Popen("wmic path win32_networkadapter\
                where index="+ str(nic.Index) +" call enable", 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
                    #sleep(5)
                    if proc.wait() == 0:
                        print(str(nic.Index) + " success enable")
                        print("MAC =", nic.MACAddress)
                        print("Name =", nic.Description)
                        print("Status =", nic.IPEnabled)
                        ind_list.append((nic.Index, nic.IPEnabled, nic.Description))
                        if nic.IPEnabled:
                            ip = "(10.0.0.num),"
                            ip = ip.replace("num", str(num))
                            num += 1
                            mask = " (255.255.255.0)"
                            print("set ip address", ip[:-1], "on", nic.Description)
                            cmd = ("wmic nicconfig where Index="+str(nic.Index)+" call EnableStatic "+ip+mask)
                            subprocess.check_output(cmd)
                        print("---------------------------------------")
        return ind_list

    def _get_data(self):
        return self.dict_info

    def _update(self, details):
        self.dict_info = details.copy()

if __name__ == '__main__':
    hw = hw_info()
    hw.usb_info()