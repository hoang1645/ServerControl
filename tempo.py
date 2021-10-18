import csv
import os
import codecs
os.system('wmic /output:list.txt process get Name, ProcessId, ThreadCount /format:csv')

csv_reader = csv.reader(codecs.open('list.txt','rU','utf-16'))
line_count = 0
for row in csv_reader:
    if len(row)==0:
        continue
    print("{},{},{},{}".format(row[0],row[1],row[2],row[3]))
    line_count += 1
print(f'Processed {line_count} lines.')