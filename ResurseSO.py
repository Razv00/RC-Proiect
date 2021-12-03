import psutil
def Cpu_Percent():
    return str(psutil.cpu_percent(interval=1))+"%"
def Cpu_Freq():
    return str(psutil.cpu_freq().current)+" Hz"
