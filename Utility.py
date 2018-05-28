from Printer import Printer


class Utility(object):

    def __init__(self, board_loc, util_name="", buy_price=0, mortgage_value=0, rent=0, pRent=0):
        self.util_name = util_name
        self.util_price = buy_price
        self.mortgage_val = mortgage_value
        self.board_location = board_loc
        self.owner = 0
        self.rent = rent
        self.paired_rent = pRent
        self.util_group = 0 # 1: Waterways+Satellite, 2: Railways+Roadways, 3: Airways+Petroleum

    def set_name(self, utility_name):
        self.util_name = utility_name

    def set_util_group(self, ids):
        self.util_group = ids

    def get_util_group(self):
        return self.util_group

    def get_util_group_name(self):
        if self.get_util_group() == 1:
            return "WS"
        elif self.get_util_group() == 2:
            return "RR"
        else:
            return "AP"

    def get_paired_rent(self):
        return self.paired_rent

    def get_name(self):
        return self.util_name

    def get_board_location(self):
        return self.board_location

    def get_mortgage_val(self):
        return self.mortgage_val

    def get_name_with_mortgage_value(self):
        return self.util_name + "(" + self.get_util_group_name() + ")" + ": $" + str(self.mortgage_val)

    def isSite(self):
        return False

    def isUtil(self):
        return True

    def get_rent(self):
        return self.rent

    def set_buy_price(self, buy_price):
        self.util_price = buy_price

    def set_mortgage_value(self, mortg_price):
        self.mortgage_val = mortg_price

    def set_ownership(self, owner_id):
        # ownership ID codes
        # 0: unsold (with bank)
        # 1: player 1
        # 2: player 2
        # 3: player 3
        # 4: player 4
        # 11: mortgaged by player 1 (with bank)
        # 12: mortgaged by player 2 (with bank)
        # 13: mortgaged by player 3 (with bank)
        # 14: mortgaged by player 4 (with bank)
        self.owner = owner_id

    def get_ownership(self):
        return self.owner

    def getBuyPrice(self):
        return self.util_price

    def __str__(self):
        return "Utility Name = %s\nUtility BuyPrice = %d\nUtility Mortgage = %d\n" % (self.util_name, self.util_price,
                                                                                      self.mortgage_val)


