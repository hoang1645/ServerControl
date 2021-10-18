import subprocess
tmp = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}")
value = tmp.decode('utf-8').split()[6:]
print(value)