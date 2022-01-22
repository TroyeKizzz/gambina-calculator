from bs4 import BeautifulSoup
import json


def convert_html_to_json(data_dir):
    # Example: data_dir = "data/2021/12/messages2"
    messages_dictionary = []
    file = open(data_dir+".html", "r")
    text = file.read()
    file.close()
    soap = BeautifulSoup(text, "html.parser")
    messages_list = soap.find_all("div", attrs={"class": "message default clearfix"})

    for i in messages_list:
        message_body = i.find("div", attrs={"class": "body"})
        if (message_body.find("div", attrs={"class": "text"})):
            msg = {
                "date": str(message_body.find("div", attrs={"class": "pull_right date details"})["title"]),
                "from_user": str(message_body.find("div", attrs={"class": "from_name"}).contents[0][1:-8]),
                "text": ""
            }

            for k in message_body.find("div", attrs={"class": "text"}).contents:
                if str(k) == "<br/>":
                    msg["text"] += " "
                elif (str(k) == "\n") or ("ShowBotCommand" in str(k)):
                    pass
                elif "href" in str(k):
                    msg["text"] += str(k.string).lower()
                elif "\n" in str(k):
                    msg["text"] += str(k).replace("\n", "").lower()
                else:
                    msg["text"] += str(k).lower()

            msg["text"] = msg["text"][:-7]
            if len(msg["text"]) < 200:
                continue

            messages_dictionary.append(msg)

    file = open(data_dir+".json", "w")
    file.write(json.dumps(messages_dictionary, indent=4, ensure_ascii=False))
    file.close()
