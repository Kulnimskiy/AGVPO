class Anton:
    def __init__(self, name) -> None:
        self.name = self.get_name(name)

    def get_name(self,name):
        return 1
    

class Friend(Anton):
    pass

def print_huy():
    return "WTF"

me = Friend(name=print_huy())
print(me.name)
        