class person:

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def setname(self, name):
        self.name = name

    def repr(self):
        return f"person({self.addr}, {self.name})"
