import os, json, lib
from win10toast import ToastNotifier

toaster = ToastNotifier()
checker = lib.WebChecker()

file_list = os.listdir("./websites")
toaster.show_toast(
    "Website checker",
    "Adding following websites:\n" + '\n'.join(file_list),
    "resources/internet.ico",
    duration=3
)
for file_name in file_list:
    with open("./websites/" + file_name, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        checker.add_target(lib.Website(
            raw_data['host'],
            raw_data['interval'],
            raw_data['condition']
        ))

toaster.show_toast(
    "Website checker",
    "Ready!",
    "resources/success.ico",
    duration=3
)
checker.start()
# while True:
#     pass
