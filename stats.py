import json
from tracemalloc import start

start_meeting_words_fin = ["avataan ajassa", "avasi kokouksen ajassa", "avasi gogouksen ajassa", "avasi gokouksen ajassa", "avaus ajassa", "avattu", "avasi", "avaa kokouksen ajassa", "kokouksen avaus", "avattiin ajassa", "avataan kokous ajassa", "kokouksen avaaminen", "alkaa ajassa", "avataan", "avatuksi", "avattu ajassa"]
start_meeting_words_eng = ["opens the meeting at", "opening of meeting", "open at", "open", "opened", "opened at"]
end_meeting_words_fin =["päätetty ajassa", "sulkeminen", "päättäminen ajassa", "päättäminen"]
end_meeting_words_eng =[]


def find_start_time(msg):
    start_time_index = -1

    # find "1. "
    found = False
    start_pos = 0
    while found == False:
        one_pos = msg.find("1.", start_pos)
        if one_pos != -1 and not(msg[one_pos+2] in "1234567890"):
            found = True
        if one_pos == -1:
            found = True
        else:
            start_pos = one_pos + 1
    
    # find "1)"
    if one_pos == -1:
        one_pos = msg.find("1)")

    # find "2. "
    found = False
    if one_pos != -1:
        start_pos = one_pos
    else:
        start_pos = 0
    while found == False:
        two_pos = msg.find("2.", start_pos)
        if two_pos != -1 and not(msg[two_pos+2] in "1234567890"):
            found = True
        if two_pos == -1:
            found = True
        else:
            start_pos = two_pos + 1

    # find "2)"
    if (one_pos == -1):
        start_pos = 0
    else:
        start_pos = one_pos + 2
    if (two_pos == -1):
        two_pos = msg.find("2)", start_pos)

    # search time between "1. " and "2. "
    if one_pos != -1 and two_pos != -1:
        time_candidates = {}
        for i in range(one_pos+4,two_pos):
            if msg[i] in "1234567890.: ":
                if msg[i-1] in "1234567890.: ":
                    time_candidates[list(time_candidates.keys())[-1]] += 1
                else:
                    time_candidates[i] = 1
        if max(list(time_candidates.values())) > 4:
            return list(time_candidates.keys())[list(time_candidates.values()).index(max(time_candidates.values()))]
    
    # search time after key words
    for word in start_meeting_words_fin + start_meeting_words_eng:
        for word2 in [word, word+" klo", word+" kello"]:
            index = msg.find(word2)
            if index != -1:
                index += len(word2)
                num = 0
                for char in msg[index:index+7]:
                    if char in "1234567890.: ":
                        num += 1
                if num > 4:
                    start_time_index = index
                    return start_time_index
    return start_time_index


def find_end_time(msg):
    end_time_index = -1

    # find "6. "
    found = False
    end_pos = 0
    while found == False:
        six_pos = msg.find("6.", end_pos)
        if six_pos != -1 and not(msg[six_pos+2] in "1234567890"):
            found = True
        if six_pos == -1:
            found = True
        else:
            end_pos = six_pos + 1
    
    # find "6)"
    if six_pos == -1:
        six_pos = msg.find("6)")

    # search time after "6. "
    if six_pos != -1:
        time_candidates = {}
        for i in range(six_pos+4,len(msg)):
            if msg[i] in "1234567890.: ":
                if msg[i-1] in "1234567890.: ":
                    time_candidates[list(time_candidates.keys())[-1]] += 1
                else:
                    time_candidates[i] = 1
        if max(list(time_candidates.values())) > 4:
            return list(time_candidates.keys())[list(time_candidates.values()).index(max(time_candidates.values()))]

    # search time after key words
    for word in end_meeting_words_fin + end_meeting_words_eng:
        for word2 in [word, word+" klo", word+" kello"]:
            index = msg.find(word2)
            if index != -1:
                index += len(word2)
                num = 0
                for char in msg[index:index+7]:
                    if char in "1234567890.: ":
                        num += 1
                if num > 4:
                    start_time_index = index
                    return start_time_index

    return end_time_index


def make_pattern(string):
    output = ""
    for i in string:
        if i in "1234567890":
            output += "0"
        elif i in ":.":
            output += ":"
        else:
            output += "_"
    return output


def convert_time(string):
    time_str = ""
    for char in string:
        if char in "1234567890.: ":
            time_str += char
            pattern = make_pattern(time_str)
    index = pattern.find("00:00")
    if index != -1:
        time_str = time_str[index:index+5].replace(".", ":")
        return time_str
    index = pattern.find("0:00")
    if index != -1:
        time_str = time_str[index:index+4].replace(".", ":")
        return time_str
    index = pattern.find("0000")
    if index != -1:
        time_str = time_str[index:index+2] + ":" + time_str[index+2:index+4]
        return time_str
    
def process_meetings(data_dir):
    # Example: data_dir = "data/2021/12/messages2"
    file = open(data_dir+".json", "r")
    messages_dictionary = json.loads(file.read())
    file.close()

    meetings = []
    unprocessed_meetings = []
    start_unprocessed_meetings = []
    end_unprocessed_meetings = []
    processed_meetings = 0
    for msg in messages_dictionary:
        meeting = {
            "message_sent_time": msg["date"],
            "start_time": "",
            "end_time": "",
            "day_of_week": ""
        }

        start_time_index = find_start_time(msg["text"])
        end_time_index = find_end_time(msg["text"])
        
        if start_time_index != -1:
            meeting["start_time"] = convert_time(msg["text"][start_time_index:start_time_index + 8])

        if end_time_index != -1:
            meeting["end_time"] = convert_time(msg["text"][end_time_index:end_time_index + 8])

        meetings.append(meeting)
        
        if start_time_index == -1 and end_time_index == -1:
            meeting["text"] = msg["text"]
            unprocessed_meetings.append(meeting)
        elif start_time_index == -1 and end_time_index != -1:
            meeting["text"] = msg["text"]
            start_unprocessed_meetings.append(meeting)
        elif start_time_index != -1 and end_time_index == -1:
            meeting["text"] = msg["text"]
            end_unprocessed_meetings.append(meeting)
        else:
            processed_meetings += 1

    file = open(data_dir+"_meetings.json", "w")
    file.write(json.dumps(meetings, indent=4, ensure_ascii=False))
    file.close()

    file = open(data_dir+"_stats.txt", "w")
    file.write("""Total number of messages: {}
        Out of them:
            - Fully processed: {}
            - Unprocessed start time: {}
            - Unprocessed end time: {}
            - Fully unprocessed: {}
    The following are the unprocessed messages: \n\n""".format(len(meetings), processed_meetings, len(start_unprocessed_meetings), len(end_unprocessed_meetings), len(unprocessed_meetings)))

    file.write("--- Fully unprocessed messages ---\n\n")
    for msg in unprocessed_meetings:
        file.write(msg["message_sent_time"]+"\n")
        file.write(msg["text"]+"\n\n")

    file.write("--- Unprocessed start time ---\n\n")
    for msg in start_unprocessed_meetings:
        file.write(msg["message_sent_time"]+"\n")
        file.write(msg["text"]+"\n\n")

    file.write("--- Unprocessed end time ---\n\n")
    for msg in end_unprocessed_meetings:
        file.write(msg["message_sent_time"]+"\n")
        file.write(msg["text"]+"\n\n")

    file.close()