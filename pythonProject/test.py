import wmi

# Initializing the wmi constructor
f = wmi.WMI()

flag = 0
print(str(i.Name) for i in f.Win32_Process())
# Iterating through all the running processes
for process in f.Win32_Process():
    if "chrome.exe" == process.Name:
        print("Application is Running")
        flag = 1
        break

if flag == 0:
    print("Application is not Running")