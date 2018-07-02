from MenuBox import MenuBox, Printer
        
class Account(object):
    
    def __init__(self, id, name, balance=0):
        self.id = id 
        self.name = name
        self.balance = balance
        self.transaction_statement = Printer()
        self.state = True
        
    def deposit(self, amount, msg=""):
        self.balance += amount
        self.statement_populate(msg, amount, 1)
        
    def withdraw(self, amount, msg=""):
        self.balance -= amount
        self.statement_populate(msg, amount, 0)
        if self.balance < 0: raise ValueError
    
    def isenoughbalance(self, amount):
        if self.balance >= amount:
            return True
        return False  
     
    def set_statement_filename(self, fname, mode):
        self.transaction_statement.set_log_file_name(fname, mode)
        self.transaction_statement.file_only_printer("{: >60} {: >8} {: >8} {: >8}".format("Transaction Details",
                                                                                           "Debit", "Credit", "Balance"))
        
    def statement_populate(self, msg, amount, type):      
        if type == 0:
            statement = "{: >60} {: >8} {: >8} {: >8}".format(msg, amount, "", self.balance)
        else:
            statement = "{: >60} {: >8} {: >8} {: >8}".format(msg, "", amount, self.balance)
        self.transaction_statement.file_only_printer(statement)

    def acc_state(self):
        return (self.id, self.balance, self.state)
    
    def change_state(self, new_state):
        (self.balance, self.state) = new_state
        
class Banksmart(object):
    
    def __init__(self, id, logPath):
        self.id = id
        self.asset_list = []
        self.accounts = [Account(0, "Bank")]
        self.logPath = logPath
        self.logObj = Printer(self.logPath)
        self.PlayerBuyMenu = MenuBox("Buy Menu", self.logPath)
        self.PlayerBuyMenu.addOption("Want to buy")
        self.PlayerMortMenu = MenuBox('Cash Raise Menu', self.logPath)
        
    def add_players_accounts(self, player_count, mode='w'):
        self.accounts[0].set_statement_filename("./business_game_logs/Bank_account_statement.txt", mode)
        for i in range(player_count):
            account_var = Account(i+1, "PL-%d" % (i+1))
            account_var.set_statement_filename("./business_game_logs/Player-%d_account_statement.txt" % (i+1), mode)
            self.accounts.append(account_var) 
            
    def get_players_balance(self, player_id):
        return self.accounts[player_id].balance
    
    def bankrupt_a_player(self, player_id):
        self.accounts[0].deposit(self.accounts[player_id].balance, "Surrendered money from Player-%d" % player_id)
        self.accounts[player_id].withdraw(self.accounts[player_id].balance, "Bankrupt")
        self.accounts[player_id].transaction_statement.file_only_printer("\nYour account has been deactivated.\n")
        prop_list = []
        for i in self.asset_list:
            if i.owner == player_id or i.owner == player_id + 10:
                prop_list.append(i.board_loc) 
                i.owner = 0
                i.prop_count = 0
                i.current_rent = i.rent
                i.prop_vacancy = False
                i.prop_sell = False
        self.accounts[player_id].state = False
        return prop_list
      
    def raise_cash(self, player_id, min_amount):
        if self.get_players_credit_value(player_id) > min_amount:
            while self.accounts[player_id].balance < min_amount:
                player_props = [i for i in self.asset_list if i.owner == player_id]            
                if len(player_props) == 0:
                    return False
                MortMenu = MenuBox('Cash Raise Menu', self.logPath)
                for i in player_props:
                    pname = ""
                    if i.issite():
                        if i.prop_count == 4:
                            pname = "(3 House, 1 Hotel)"
                        elif 1 <= i.prop_count < 4:
                            pname = "(%d House)" % i.prop_count
                        else:
                            pname = ""
                    MortMenu.addOption(i.name + " " + pname ) 
                opt = MortMenu.runMenu()
                print "you selected " + str(opt)
                if player_props[opt-1].issite():
                    if player_props[opt-1].prop_count > 0:
                        self.get_building_from_player(player_id, player_props[opt-1].board_loc)
                    else:
                        self.mortgage_asset_of_player(player_id, player_props[opt-1].board_loc)
                else:
                    self.mortgage_asset_of_player(player_id, player_props[opt-1].board_loc)
            return True
        else:
            return False
        
    def get_players_asset_value(self, player_id):
        return reduce(lambda x, y: x + y, [i.buy_price if i.owner == player_id or i.owner == player_id + 10 else 0 for i in self.asset_list])

    def get_players_valuation(self, player_id):
        val = 0
        for i in self.asset_list:
            if i.owner == player_id:
                val += i.buy_price
            elif i.owner == player_id + 10:
                val += i.buy_price - (i.mortgage_val * 1.1)
            else:
                pass
        return val + self.accounts[player_id].balance        
    
    def get_players_credit_value(self, player_id):
        return reduce(lambda x, y: x + y, [self.accounts[player_id].balance] + [i.mortgage_val for i in self.asset_list if i.owner == player_id] + 
                [(i.prop_price * i.prop_count) / 2 for i in self.asset_list if i.owner == player_id if i.issite()])
        
    def get_owner_by_assetid(self, id):
        for i in self.asset_list:
            if i.board_loc == id:
                return i.owner
        return -1    
                
    def get_asset_by_assetid(self, asset_id):
        return filter(lambda x: x.board_loc == asset_id, self.asset_list)[0]
    
    def get_players_countries(self, player_id):
        return len([i for i in self.asset_list if i.issite() if i.owner == player_id or i.owner == player_id + 10])
    
    def get_players_mort_assets(self, player_id):
        return len([i for i in self.asset_list if i.owner == player_id + 10])        
        
    def get_current_rent_by_assetid(self, id):
        asset = self.get_asset_by_assetid(id)          
        if asset.issite():
            if asset.prop_count == 0:
                color_count = len([1 for i in self.asset_list if i.issite() if i.owner == asset.owner and i.color_grp == asset.color_grp])
                if color_count >= 3:
                    return asset.current_rent * 2 
            return asset.current_rent
        else:
            grp_count = len([1 for i in self.asset_list if i.issite() is False if i.owner == asset.owner and i.pair_grp == asset.pair_grp])
            if grp_count == 2:
                return asset.pair_rent
            return asset.current_rent             
     
    def group_wise_asset_list(self, player_id):
        color_code = ('R', 'G', 'B', 'Y', 'U')
        prop_name_list = [[],[],[],[],[]]
        for i in self.asset_list:
            if i.owner == player_id:
                if i.issite():
                    prop_name_list[i.color_grp-1].append(i.get_name_with_prop_flag())
                else:
                    prop_name_list[4].append(i.name)
            elif i.owner == player_id + 10:
                if i.issite():
                    prop_name_list[i.color_grp-1].append(i.get_name_with_prop_flag() + '(m)')
                else:
                    prop_name_list[4].append(i.name + '(m)')
            else: pass
        return (", ".join(['%s:%d' % (color_code[i], len(prop_name_list[i])) for i in range(5)]) + " ## " 
                + ' '.join(['%s:%s' % (color_code[i], ",".join(prop_name_list[i])) for i in range(5) if len(prop_name_list[i]) > 0])) 
               
    def sell_asset_to_player(self, player_id, asset_id):
        asset = self.get_asset_by_assetid(asset_id)
        if asset.owner == 0:
            self.logObj.printer("You reached on %s\n" % asset.name)
            player_mort_assets = self.get_players_mort_assets(player_id)
            if player_mort_assets == 0:
                if self.accounts[player_id].isenoughbalance(asset.buy_price):
                    player_buyconsent = self.PlayerBuyMenu.runMenu() 
                    if player_buyconsent == 1:
                        self.accounts[player_id].withdraw(asset.buy_price, "Asset %s purchase from Bank" % asset.name)
                        self.accounts[0].deposit(asset.buy_price, "Asset %s sale to Player-%d" % (asset.name, player_id))
                        asset.owner = player_id
                        self.prop_vacancy_set(player_id, asset)
                        self.logObj.printer("Purchase done")    
                        return 0 
                    else:
                        self.logObj.printer("Player-%d not interested in purchase." % player_id)
                else:
                    self.logObj.printer("Player-%d has not sufficient balance to buy." % player_id)
            else:
                self.logObj.printer('You have already mortgaged %d assets to bank.\nYou can not buy any property till you have any mortgaged one.\n' % player_mort_assets)
        elif asset.owner == player_id:
            self.logObj.printer("You reached on your own property")
        elif asset.owner < 10:
            rent = self.get_current_rent_by_assetid(asset_id) 
            self.logObj.printer("You reached on %s which attracts rent of $%d" % (asset.name, rent))
            if self.accounts[player_id].isenoughbalance(rent) is False:
                if self.raise_cash(player_id, rent):
                    pass
                else:
                    return -1 # return -1 for removing the player                         
            self.accounts[player_id].withdraw(rent, "Asset %s rent to Player-%d" % (asset.name, asset.owner))
            self.accounts[asset.owner].deposit(rent, "Asset %s rent from Player-%d" % (asset.name, player_id)) 
            return 1 
        else:
            self.logObj.printer("You reached on a mortgaged property. No need to pay any rent.")            
        return 1             
        
    
    def sell_building_to_player(self, player_id, asset_id):
        asset = self.get_asset_by_assetid(asset_id)
        if asset.owner == player_id:
            if asset.prop_vacancy:
                if self.accounts[player_id].isenoughbalance(asset.prop_price):
                    try:
                        asset.prop_count += 1
                        self.accounts[player_id].withdraw(asset.prop_price, "Building purchase on %s" % asset.name)
                        self.accounts[0].deposit(asset.prop_price, "Building sale to Player-%d" % player_id)
                        self.prop_vacancy_set(player_id, asset)
                        self.prop_sell_set(player_id, asset)
                        self.logObj.printer("Building purchase done. Remaining balance = $%d" % self.accounts[player_id].balance) 
                    except ValueError:
                        self.logObj.printer("You can not raise more buildings on %s. Already 4." % asset.name)            
                else:
                    self.logObj.printer("You don't have sufficient balance to raise building on %s" % asset.name)
            else:
                self.logObj.printer("No more building allowed on %s. It has either 4 buildings or more building " \
                                    "than your other sites of same color." % asset.name) 
        elif asset.owner == player_id + 10:
            self.logObj.printer("You can not raise building on your mortgaged property (%s)." % asset.name) 
        else:
            self.logObj.printer("You can not raise building on property (%s) as not owner." % asset.name)
            
           
    def get_building_from_player(self, player_id, asset_id):
        asset = self.get_asset_by_assetid(asset_id)
        if asset.owner == player_id:
            sell_price = asset.prop_price / 2
            if asset.prop_sell:
                if self.accounts[0].isenoughbalance(sell_price):
                    try:
                        asset.prop_count -= 1
                        self.accounts[0].withdraw(sell_price, "Building re-purchase from Player-%d" % player_id)
                        self.accounts[player_id].deposit(sell_price, "Building sale from %s" % asset.name)
                        self.prop_vacancy_set(player_id, asset)
                        self.prop_sell_set(player_id, asset)
                        self.logObj.printer("Building sell done. Remaining balance = $%d" % self.accounts[player_id].balance)
                    except ValueError:
                        self.logObj.printer("You can not sell more buildings on %s. Already 0." % asset.name)            
                else:
                    self.logObj.printer("Bank doesn't have sufficient balance to purchase your building on %s" % asset.name)
            else:
                self.logObj.printer("You can not sell buildings on %s as it has no building or lesser buildings " \
                                    "than your other properties of same color." % asset.name)   
        else:
            self.logObj.printer("You can not sell buildings on %s as not owner." % asset.name)     
            raise ValueError
            
    def mortgage_asset_of_player(self, player_id, asset_id):
        asset = self.get_asset_by_assetid(asset_id)
        if asset.owner == player_id:
            mort_amount = asset.mortgage_val
            if self.accounts[0].isenoughbalance(mort_amount):
                asset.owner = player_id + 10
                asset.prop_vacancy = False
                self.accounts[0].withdraw(mort_amount, "Asset %s mortgage from Player-%d" % (asset.name, player_id))
                self.accounts[player_id].deposit(mort_amount, "Asset %s mortgaged to bank" % asset.name)
                self.logObj.printer("Asset mortgage done. Remaining balance = $%d" % self.accounts[player_id].balance)
            else:
                self.logObj.printer("Bank doesn't have sufficient balance to give mortgage value of %s" % asset.name)
        else:
            self.logObj.printer("You can not mortgage other player's asset")   
            print "player id = %d" % player_id
            print "asset id = %d" % asset_id
            raise ValueError
        
    def redeem_asset_of_player(self, player_id, asset_id):
        asset = self.get_asset_by_assetid(asset_id)
        if asset.owner == player_id + 10:
            mort_amount = int(asset.mortgage_val * 1.1)
            if self.accounts[player_id].isenoughbalance(mort_amount):
                asset.owner = player_id
                self.prop_vacancy_set(player_id, asset)
                self.prop_sell_set(player_id, asset)
                self.accounts[player_id].withdraw(mort_amount, "Asset %s redeemed from Bank" % (asset.name))
                self.accounts[0].deposit(mort_amount, "Asset %s redeemed by Player-%d" % (asset.name, player_id))
                self.logObj.printer("Asset redemption done. Remaining balance = $%d" % self.accounts[player_id].balance)
            else:
                self.logObj.printer("Player-%d doesn't have sufficient balance to redeem %s" % (player_id, asset.name))
        else:
            self.logObj.printer("You can not redeem other player's mortgaged asset." % asset.name)   
            raise ValueError

    def prop_vacancy_set(self, player_id, asset):
        if asset.issite():
            col_grp_count = len([1 for i in self.asset_list if i.issite() if i.owner == player_id and i.color_grp == asset.color_grp])
            if col_grp_count >= 3:
                prop_cnt_list = [i.prop_count for i in self.asset_list if i.issite() if i.owner == player_id and i.color_grp == asset.color_grp]
                fl_list = [True if i == min(prop_cnt_list) and min(prop_cnt_list) != 4 else False for i in prop_cnt_list]
                for i in self.asset_list:
                    if i.issite():
                        if i.owner == player_id and i.color_grp == asset.color_grp:
                            i.prop_vacancy = fl_list[0]
                            del fl_list[0]     
                
    def prop_sell_set(self, player_id, asset):
        if asset.issite():
            prop_cnt_list = [i.prop_count for i in self.asset_list if i.issite() if i.owner == player_id and i.color_grp == asset.color_grp]
            fl_list = [True if i == max(prop_cnt_list) and max(prop_cnt_list) != 0 else False for i in prop_cnt_list]
            for i in self.asset_list:
                if i.issite():
                    if i.owner == player_id and i.color_grp == asset.color_grp:
                        i.prop_sell = fl_list[0]
                        del fl_list[0]
                                      
    def payreward(self, player_id, amount, msg): 
        if self.accounts[0].isenoughbalance(amount) is False:
            return [0]
        self.accounts[0].withdraw(amount, msg)
        self.accounts[player_id].deposit(amount, msg)
        return []

    def p2ptransaction(self, payee_id, recep_id, amount, msg):
        if amount == -1:
            factor = 1
            if msg == "custom duty": factor = 2
            amount = self.get_players_countries(payee_id) * 50 * factor
            if amount > 500 * factor:
                amount = 500 * factor   
        if self.accounts[payee_id].isenoughbalance(amount) is False:
            if self.raise_cash(payee_id, amount) is False:
                return [payee_id]
        self.accounts[payee_id].withdraw(amount, msg)
        self.accounts[recep_id].deposit(amount, msg)
        return []
