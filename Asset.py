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
    
    def isutil(self):
        return False
    
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
            prefix = "(h" + str(self.prop_counter) + ")"
        elif self.prop_count == 4:
            prefix = "(ht)"
        else:
            prefix = ""
        return self.name + prefix
    
    def state(self):
        return (self.board_loc, self.owner, self.current_rent, self.prop_count, self.prop_vacancy, self.prop_sell)
            
        
class Utility(Asset):
    def __init__(self, board_loc, name, buy_price, mortgage_value, rent, pair_rent, grp):
        super(Utility, self).__init__(board_loc, name, buy_price, mortgage_value, rent)
        self.pair_rent = pair_rent  
        self.current_rent = self.rent
        self.pair_grp = grp
        
    def issite(self):
        return False
    
    def isutil(self):
        return True
    
    def state(self):
        return (self.board_loc, self.owner, self.current_rent)
