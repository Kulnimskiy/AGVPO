import win32com.client
import csv

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

folder_name = input("Название папки где лежат письма: ")
email_sender = input("Почта адресс: ")


# "6" refers to the index of a folder - in this case,
# the inbox. You can change that number to reference
# any other folder

def get_messages_info():
    inbox = outlook.Folders.Item(1).Folders[folder_name]
    all_people = []
    for message in inbox.Items:
        try:
            if message.SenderEmailAddress == email_sender and "Request details:" in message.body:
                message = message.body.split("Request details:")[1].split("Additional information:")[0]
                message = message.split("\r\n")
                main_info = dict()
                for pair in message:
                    if ":" in pair and pair.count(":") == 1:
                        k, v = pair.split(":")
                        main_info[k.strip()] = v.strip()
                all_people.append(main_info)
        except Exception:
            print("skip")
    return all_people


messages = get_messages_info()
fieldNames = []
for person in messages:
    fieldNames.extend(person.keys())
fieldNames = sorted(list(set(fieldNames)))
with open('info.csv', 'w', newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldNames, delimiter=' ')
    writer.writeheader()
    for person in messages:
        writer.writerow(person)

