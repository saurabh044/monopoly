class Asset(object):
    
    def __init__(self, board_loc, name, buy_price, mortgage_value, rent):
        self.board_loc = board_loc
        self.name = name
        self.buy_price = buy_price
        self.mortgage_val = mortgage_value
        self.rent = rent
        self.owner = 0        
    
class Country(Asset):
    
    def __init__(self, board_loc, name, buy_price, mortgage_value, rent, prop_price, prop_rent, grp):
        super(Country, self).__init__(board_loc, name, buy_price, mortgage_value, rent)
        self.prop_price = prop_price
        self.prop_rent = prop_rent
        self.prop_count = 0
        self.current_rent = self.rent
        self.color_grp = grp
        self.prop_vacancy = False
        self.prop_sell = False
    
    def issite(self):
        return True

    @property
    def prop_count(self):
        return self._prop_count
    
    @prop_count.setter
    def prop_count(self, value):
        if 0 <= value <= 4:
            self._prop_count = value
            if 1 <= value <= 3:
                self.current_rent = self.prop_rent * value
            elif value == 4:
                self.current_rent = self.prop_rent * 3 + 1000
                self.prop_vacancy = False
            else:
                self.current_rent = self.rent
                self.prop_sell = False
        else:
            raise ValueError
        
    def get_name_with_prop_flag(self):
        if 1 <= self.prop_count <= 3:
            prefix = "(h" + str(self.prop_count) + ")"
        elif self.prop_count == 4:
            prefix = "(ht)"
        else:
            prefix = ""
        return self.name + prefix
    
    def state(self):
        return (self.board_loc, self.owner, self.current_rent, self.prop_count, self.prop_vacancy, self.prop_sell)
    
    def change_state(self, new_state):
        (self.owner, self.current_rent, self.prop_count, self.prop_vacancy, self.prop_sell) = new_state
        
    def info(self):
        col = ('Red', 'Green', 'Blue', 'Yellow')
        if self.owner == 0:
            owner = 'Bank'
        elif self.owner < 10:
            prop_vac, prop_sel = ('No', 'No')
            if self.prop_vacancy == True: prop_vac = 'Yes'
            if self.prop_sell == True: prop_sel = 'Yes'
            owner = 'Player-%d\nCurrent Rent =%d\nTotal Properties = %d\nCan raise property = %s\nCan sell property = %s\n' % (self.owner, 
                        self.current_rent, self.prop_count, prop_vac, prop_sel)
        else:
            owner = 'Player-%d has mortgaged to bank.' % (self.owner - 10)
        return "Country Name = %s\n--------------------\nColor Group = %s\nBoard Location = %d\nMortgage Value = %d\nBasic Rent = %d\nRent in color triplet = %d\nCurrent Owner = %s" % (self.name, 
                col[self.color_grp - 1], self.board_loc, self.mortgage_val, self.rent, (2 * self.rent), owner)

        
class Utility(Asset):
    def __init__(self, board_loc, name, buy_price, mortgage_value, rent, pair_rent, grp):
        super(Utility, self).__init__(board_loc, name, buy_price, mortgage_value, rent)
        self.pair_rent = pair_rent  
        self.current_rent = self.rent
        self.pair_grp = grp
        
    def issite(self):
        return False
    
    def state(self):
        return (self.board_loc, self.owner, self.current_rent)
    
    def change_state(self, new_state):
        (self.owner, self.current_rent) = new_state

    def info(self):
        if self.owner == 0:
            owner = 'Bank'
        elif self.owner < 10:
            owner = 'Player-%d\nCurrent Rent =%d\n' % (self.owner, self.current_rent)
        else:
            owner = 'Player-%d has mortgaged to bank.' % (self.owner - 10)
        return "Utility Name = %s\n--------------------\nBoard Location = %d\nMortgage Value = %d\nBasic Rent = %d\nRent with pair = %d\nCurrent Owner = %s" % (self.name, 
                self.board_loc, self.mortgage_val, self.rent, self.pair_rent, owner)
