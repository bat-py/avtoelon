class Super:
    def __init__(self):
        print("asshole")

class Daughter(Super):
    def __init__(self):
        print("Welcome to Daghter Class")
        super().__init__()


Daughter()