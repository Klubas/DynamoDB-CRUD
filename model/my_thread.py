import sys
import threading
import subprocess

class myThread (threading.Thread):
    def __init__(self, threadID, value):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.returnCode = -1
    def run(self):
        s = subprocess.Popen(["python", self.value])
        s.wait()
        self.returnCode = s.returncode