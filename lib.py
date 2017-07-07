import time

import requests
import sched
from win10toast import ToastNotifier


class Website:
    def __init__(self, host, interval, condition):
        self.host = host
        self.interval = interval
        self.condition = condition
        self.toaster = ToastNotifier()

        self.last_result = None

    def check(self):
        r = requests.request("GET", self.host, headers={
            "Accept-Charset": "utf-8"
        }, stream=True)
        print(self.host + "\n>  Status code:", r.status_code)
        if r.status_code == 200:
            if "not_contains" in self.condition:
                print(self.condition['includes'])
                if r.text.find(self.condition['includes']) == -1:
                    return False
            if "line_equals" in self.condition:
                print(self.condition['line_equals'])
                for line in r.iter_lines():
                    print(line)
                    if line == self.condition['line_equals']:
                        return True
                    return False
            if "first_line_not_equals" in self.condition:
                print(self.condition["first_line_not_equals"])
                for line in r.iter_lines(decode_unicode=True):
                    print(line)
                    if line is self.condition['first_line_not_equals']:
                        return False
            if "size_more_than" in self.condition:
                length = len(r.text)
                print(self.condition["size_more_than"], " vs real", length)
                if length < self.condition["size_more_than"]:
                    return False
            return True
        return False

    def check_and_notify(self):
        new_result = self.check()
        if self.last_result is None or new_result != self.last_result:
            self.last_result = new_result
            if new_result:
                self.toaster.show_toast(
                    "Website checker",
                    self.host + " is available!",
                    icon_path="resources/success.ico",
                    duration=10
                )
            else:
                self.toaster.show_toast(
                    "Website checker",
                    self.host + " is down!",
                    icon_path="resources/error.ico",
                    duration=10
                )


class WebChecker:
    def __init__(self):
        self.websites = []
        self.loop = sched.scheduler(time.time, time.sleep)
        self.event_ids = []

    def add_target(self, website):
        self.websites.append(website)
        self.event_ids.append(self.loop.enter(website.interval, 1, self.worker, (website,)))

    def start(self):
        self.loop.run(True)

    def stop(self):
        for event in self.event_ids:
            self.loop.cancel(event)

    def worker(self, website):
        website.check_and_notify()
        self.loop.enter(website.interval, 1, self.worker, (website,))
