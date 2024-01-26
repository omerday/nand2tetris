class Symbols:
    symbols = {}
    next_free = 0

    def __init__(self):

        self.symbols = {"SCREEN": 16384,
                        "KBD": 24576,
                        "SP": 0,
                        "LCL": 1,
                        "ARG": 2,
                        "THIS": 3,
                        "THAT": 4}

        for i in range(0, 16):
            self.symbols[f"R{i}"] = i

        self.next_free = 16

    def add_entry(self, symbol: str, address=0):
        if symbol not in self.symbols.keys():
            if address != 0:
                self.symbols[symbol] = address
            else:
                self.symbols[symbol] = self.next_free
                self.next_free += 1
                # while self.next_free in self.symbols.values():
                #     self.next_free += 1
                return self.symbols[symbol]

    def contain(self, symbol: str):
        return symbol in self.symbols.keys()

    def get_address(self, symbol: str):
        if self.contain(symbol):
            return self.symbols[symbol]
        else:
            return -1
