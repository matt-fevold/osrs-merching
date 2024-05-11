class Item:
    def __init__(self, id, name, limit, members, high_alch):
        self.id = int(id)
        self.name = name
        self.limit = limit
        self.members = members
        self.high_alch = high_alch

    # probably a way to have output as json already, too lazy to lookup atm.
    def __str__(self):
        return "{\n\tid : " + str(self.id) + ",\n\tname : " + str(self.name) + ",\n\tlimit : " + str(self.limit) + ",\n\tmembers : " + str(self.members) + ",\n\thigh_alch : " + str(self.high_alch) + ",\n}"
