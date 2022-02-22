from html_to_json import *
from stats import *

data_dir = "data/2021/"
mode = 1

'''
modes:
0 - regenerate all the data
1 - generate a report
'''

def mode0():
    for i in range(1, 13):
        print("Dir: "+data_dir+str(i)+"/messages")
        convert_html_to_json(data_dir+str(i)+"/messages")
        process_meetings(data_dir+str(i)+"/messages")
        try:
            print("Dir: "+data_dir+str(i)+"/messages2")
            convert_html_to_json(data_dir+str(i)+"/messages2")
            process_meetings(data_dir+str(i)+"/messages2")
        except:
            print("Error: directory does not exist: \n\t"+data_dir+str(i)+"/messages2")

def mode1():
    stats = []
    for i in range(1, 13):
        print("Dir: "+data_dir+str(i)+"/messages")
        stats.append(extract_stats(data_dir+str(i)+"/messages"))
        try:
            print("Dir: "+data_dir+str(i)+"/messages2")
            stats.append(extract_stats(data_dir+str(i)+"/messages2"))
        except:
            print("Error: directory does not exist: \n\t"+data_dir+str(i)+"/messages2")
    
    total = 0
    monthly = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in stats:
        total += i["processed"]
        total += i["start_unprocessed"]
        total += i["end_unprocessed"]
        monthly[i["month"]-1] += i["processed"]
        monthly[i["month"]-1] += i["start_unprocessed"]
        monthly[i["month"]-1] += i["end_unprocessed"]

    print(total, monthly)

    for i in monthly:
        print(i)



if mode == 0:
    mode0()
elif mode == 1:
    mode1()
