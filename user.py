import sys

class User():
    def __init__(self):
        self.email = ""
        self.username = None
        self.last_name = None
        self.first_name = None
        self.conta = None

    def resetEmail(self):
        self.email = ""
    
    def emailVazio(self):
        if self.email == "":
            return True
        else:
            return False