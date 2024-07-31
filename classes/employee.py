import sqlite3

class Employee:
    
    def __init__(self, first, last, status, project, starting, phone_number):
        self.first = first
        self.last = last
        self.phone_number = phone_number

        self.status = status
        self.project = project
        self.starting = starting
        self.phone_number = phone_number

    @property
    def email(self):
        return "{}.{}@aalto.fi".format(self.first, self.last)
    
    @property
    def fullname(self):
        return "{} {}".format(self.first, self.last)
    
    def __repr__(self):
        return "Employee({}, {}, {}, {})".format(self.first, self.last, self.status, self.project)
    
        
if __name__ == "__main__":

    try:
        person = Employee("first", "last", "status", "project", "starting", "phone_number")
        print("Employee class created")
    except:
        print("Employee class failed")