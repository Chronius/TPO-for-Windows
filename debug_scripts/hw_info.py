import wmi

Drive_Type = {"Unknown" : 0, "No Root Directory" : 1, "Local Disk" : 2,
             "Network Drive" : 3, "Compact Disc" : 4, "RAM Disk" : 5}


class hw_info():
    def __init__(self):
        self.w = wmi.WMI()
        self.list_info = [arg for arg in dir(self) if (callable(getattr(self, arg)) \
                                                and not arg.startswith('_'))]

        self.dict_info = dict((k, False) for k in self.list_info)

    #return list of tuples [(Type0, Name0), (Type1, Name1), ...]
    def disk_info(self):
        disk_list = []
        for disk in self.w.Win32_DiskDrive():
            if "SanDisk Ultra" in disk.Model or "Virtual Disk" in disk.Model:
                continue
            print("Name =", disk.Name)
            print("Model =", disk.Model)
            print("MediaType =", disk.MediaType)
            size = (int(disk.Size)/pow(1024,3))
            print("Size =", round(size, 2), "Gbyte")
            print("Sector size =", disk.BytesPerSector)
            print("Serial number =", disk.SerialNumber)
            print("InterfaceType =", disk.InterfaceType, "\n")
            disk_list.append((disk.Name, disk.Model))
        return disk_list

    def com_info(self):
        for port in self.w.Win32_SerialPort():
            print("Name =", port.Name)
            print("ProviderType =", port.ProviderType)
            print("MaxBaudRate =", port.MaxBaudRate)
            print("Status =", port.Status, "\n")

    def ram_info(self):
        for dev in self.w.Win32_PhysicalMemory():
            print("Name =", dev.Name)
            print("Manufacturer =", dev.Manufacturer)
            size = int(dev.Capacity)/pow(1024, 3)
            print("Capacity =", size, "Gbyte")
            print("DeviceLocator =", dev.DeviceLocator)
            print("SerialNumber =", dev.SerialNumber)
        for dev in self.w.Win32_PerfFormattedData_PerfOS_Memory():
            print("Memory free =", dev.AvailableMbytes, "Mb")
            print("")

    def usb_info(self):
        for hub in self.w.Win32_USBController():
            print(hub.Name)
        print("")

    def gpu_info(self):
        for gpu in self.w.Win32_VideoController():
            print("Name =", gpu.Name)
            print("Hight =",gpu.CurrentVerticalResolution)
            print("Wedght =", gpu.CurrentHorizontalResolution)
            print("")

    def voltage_info(self):
        for v in self.w.Win32_VoltageProbe():
            print(v)

    def temp_info(self):
        for temp in self.w.Win32_Processor():
            print(temp.CurrentVoltage)
            print("")

    def cpu_info(self):
        for cpu in self.w.Win32_Processor():
            print(cpu.Name)
            print("CPU Family =", cpu.Caption)
            print("NumberOfCores =", cpu.NumberOfCores)
            print("L2CacheSize =", cpu.L2CacheSize)
            print("L3CacheSize =", cpu.L3CacheSize)
            print("CurrentClockSpeed =", cpu.CurrentClockSpeed)
            print("CPU load =", cpu.LoadPercentage, "%\n")

    def pci_info(self):
        for f in self.w.Win32_PnPEntity():
            if f.DeviceID and f.Name and "PCI" in f.DeviceID \
            and not "Стандартный" in f.Name:
                print(f.Name)
        print("")

    def display_info(self):
        for d in self.w.Win32_DesktopMonitor():
            print("Name =", d.Name)
            print("Device ID =", d.DeviceID)
            print("ScreenHeight =", d.ScreenHeight)
            print("ScreenWidth =", d.ScreenWidth)
            print("")

    def foo(self):
        print(self.dict_info)

    def _get_data(self):
        return self.dict_info

    def _update(self, details):
        self.dict_info = details.copy()