from Printer import Printer


class Country(object):

    def __init__(self, grp, board_loc, country_name="", buy_price=0, mortgage_value=0, rent=0, prop_price=0, prop_rent=0):
        self.country_name = country_name
        self.country_price = buy_price
        self.mortgage_val = mortgage_value
        self.board_location = board_loc
        self.owner = 0
        self.group = grp
        self.rent = rent
        self.site_only_rent = rent
        self.property_price = prop_price
        self.prop_rent = prop_rent
        self.prop_counter = 0

    def set_name(self, country_name):
        self.country_name = country_name

    def get_board_location(self):
        return self.board_location

    def get_group(self):
        return self.group

    def get_rent(self):
        return self.rent

    def set_rent(self, amount):
        self.rent = amount

    def get_property_count(self):
        return self.prop_counter

    def get_property_code(self):
        if 1 <= self.get_property_count() <= 3:
            return "(h%d)" % self.get_property_count()
        elif self.get_property_count() == 4:
            return "(ht)"
        else:
            return "(h0)"

    def add_one_property(self):
        if self.prop_counter < 4:
            self.prop_counter += 1
            if 1 <= self.prop_counter <= 3:
                self.set_rent(self.prop_counter * self.prop_rent)
            elif self.prop_counter == 4:
                self.set_rent((3 * self.prop_rent) + 1000)
            else:
                pass
            return self.prop_counter
        else:
            return 0

    def reduce_one_property(self):
        if self.prop_counter > 0:
            self.prop_counter -= 1
            if 1 <= self.prop_counter <= 3:
                self.set_rent(self.prop_counter * self.prop_rent)
            elif self.prop_counter == 0:
                self.set_rent(self.site_only_rent)
            else:
                pass
            return self.prop_counter
        else:
            return 5

    def get_group_code(self):
        if self.get_group() == 1:
            return "R"
        elif self.get_group() == 2:
            return "G"
        elif self.get_group() == 3:
            return "B"
        else:
            return "Y"

    def get_group_color_name(self):
        if self.get_group() == 1:
            return "Red"
        elif self.get_group() == 2:
            return "Green"
        elif self.get_group() == 3:
            return "Blue"
        else:
            return "Yellow"

    def get_building_price(self):
        return self.property_price

    def get_building_selling_price(self):
        return self.get_building_price() / 2

    def get_name_with_mortgage_value(self):
        return self.country_name + "(" + self.get_group_code() + ")" + self.get_property_code() + ": $" + str(self.mortgage_val)

    def get_name_with_single_building_sell_value(self):
        return self.country_name + "(" + self.get_group_code() + ")" + self.get_property_code() + ": $" + str(self.get_building_price()/2)

    def get_name_with_building_price(self):
        return self.country_name + "(" + self.get_group_code() + ")" + self.get_property_code() + ": $" + str(self.property_price)

    def get_mortgage_val(self):
        return self.mortgage_val

    def get_name(self):
        return self.country_name

    def get_name_with_prop_flag(self):
        if 1 <= self.prop_counter <= 3:
            prefix = "(h" + str(self.prop_counter) + ")"
        elif self.prop_counter == 4:
            prefix = "(ht)"
        else:
            prefix = ""
        return self.get_name() + prefix

    def isSite(self):
        return True

    def isUtil(self):
        return False

    def set_buy_price(self, buy_price):
        self.country_price = buy_price

    def set_mortgage_value(self, mortg_price):
        self.mortgage_val = mortg_price

    def set_country_color_group(self, grp):
        # Group ID:
        # Red : 1
        # Green : 2
        # Blue : 3
        # Yellow : 4
        self.group = grp

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
        return self.country_price

    def __str__(self):
        if self.group == 1:
            col = "Red"
        elif self.group == 2:
            col = "Green"
        elif self.group == 3:
            col = "Blue"
        else:
            col = "Yellow"
        return "Country Group = %s\nCountry Name = %s\nCountry BuyPrice = %d\nCountry Mortgage = %d\n" % (col, self.country_name, self.country_price, self.mortgage_val)

