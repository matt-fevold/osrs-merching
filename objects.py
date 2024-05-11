class Item:
    def __init__(self, id, name, limit, members, high_alch):
        self.low_time = None
        self.low_price = None
        self.high_time = None
        self.high_price = None
        self.id = int(id)
        self.name = name
        self.limit = limit
        self.members = members
        self.high_alch = high_alch

    # probably a way to have output as json already, too lazy to lookup atm.
    def __str__(self):
        return ("{\n\tid : " + str(self.id) +
                ",\n\tname : " + str(self.name) +
                ",\n\tlimit : " + str(self.limit) +
                ",\n\tmembers : " + str(self.members) +
                ",\n\thigh_alch : " + str(self.high_alch) +
                ",\n\thigh_price : " + str(self.high_price) +
                ",\n\tlow_price : " + str(self.low_price) +
                ",\n\thigh_time : " + str(self.high_time) +
                ",\n\tlow_time : " + str(self.low_time) +
                ",\n}")

    def add_price_data(self, high_price, high_time, low_price, low_time):
        self.high_price = high_price
        self.high_time  = high_time
        self.low_price = low_price
        self.low_time  = low_time