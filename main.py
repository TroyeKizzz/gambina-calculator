from ast import Try
from html_to_json import *
from stats import *

data_dir = "data/2021/"


for i in range(1, 13):
    print("Dir: "+data_dir+str(i)+"/messages")
    convert_html_to_json(data_dir+str(i)+"/messages")
    process_meetings(data_dir+str(i)+"/messages")
    try:
        print("Dir: "+data_dir+str(i)+"/messages2")
        convert_html_to_json(data_dir+str(i)+"/messages2")
        process_meetings(data_dir+str(i)+"/messages2")
    except:
        pass