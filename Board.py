from Country import Country
from Utility import Utility
from Printer import Printer


class Board(object):

    def __init__(self, logPath):
        self.place_count = 36
        self.logObj = Printer(logPath)
        self.positions = ["Start",
                          "England R($2500)#", "Iraq G($5000)+", "Waterways ($9500)",
                          "UNO", "France R($2500)#", "Iran G($2500)+", "Satellite ($2000)", "Egypt G($3200)+",
                          "Resort", "Canada Y($4000)%", "Germany R($3500)#", "Airways ($10500)",
                          "Custom Duty", "Swiss R($3500)#", "Brazil Y($2500)%",
                          "Chance", "Italy R($3500)#", "Party House", "Japan B($2500)^",
                          "USA Y($8500)%", "Travelling Duty", "Roadways ($3500)", "Mexico Y($4000)%",
                          "Hongkong B($2000)^", "UNO", "Australia Y($3300)%", "Jail",
                          "India B($5500)^", "Chance", "SaudiArab G($5500)+", "Petroleum ($5500)",
                          "China B($4500)^", "Railways ($9500)", "Malaysia G($1500)+", "Singapore B($3000)^"]
        self.players_location = []

    def display_board(self):
        i = 0
        while i < self.place_count:
            u = 0
            loc = ""
            if self.players_location.count(i+1) > 0:
                u = 0
                loc = ""
                for j in self.players_location:
                    u += 1
                    if (i+1) == j:
                        loc = loc + "<P" + str(u) + "> "
            self.logObj.printer("{: <20} {: >20} {: >20}".format(str(i+1), self.positions[i], loc))
            i += 1
        self.logObj.printer("")

    def set_players_position(self, position):
        self.players_location = position







