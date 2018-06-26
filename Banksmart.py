from Printer import Printer


class Transaction(object):
   
    def __init__(self, payee, recipient, type, detail, msg):
        self.payee = payee
        self.recipient = recipient
        self.type = type 
        self.detail = detail
        self.msg = msg  
        
class Account(object):
    
    def __init__(self, id, name, balance=0):
        self.id = id 
        self.name = name
        self.balance = balance
        self.transaction_statement = Printer()
        self.state = True
        
    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        self.balance -= amount
    
    def isenoughbalance(self, amount):
        if self.balance >= amount:
            return True
        return False  
    
    def deactivate(self):
        self.state = False   
    
#     @property
#     def id(self):
#         if self._id == 0:
#             return "Bank"
#         else:
#             return 'Player-%d' % self._id
#         
#     @id.setter
#     def id(self, value):
#         self._id = value
#     
    def set_statement_filename(self, fname):
        self.transaction_statement.set_log_file_name(fname)
        self.transaction_statement.file_only_printer("{: >60} {: >8} {: >8} {: >8}".format("Transaction Details",
                                                                                           "Debit", "Credit", "Balance"))
        
class Banksmart(object):
    
    def __init__(self, id):
        self.id = id
        self.asset_list = []
        self.accounts = [Account(0, "Bank")]
        self.accounts[0].set_statement_filename("./business_game_logs/Bank_account_statement.txt")
       
    def add_players_accounts(self, player_count):
        for i in range(player_count):
            account_var = Account(i+1, "PL-%d" % (i+1))
            account_var.set_statement_filename("./business_game_logs/Player-%d_account_statement.txt" % (i+1))
            self.accounts.append(account_var) 
            
    def get_players_balance(self, player_id):
        return self.accounts[player_id].balance
    
    def get_players_asset_value(self, player_id):
        val = 0
        for i in self.asset_list:
            if i.owner == player_id:
                val += i.buy_price
        return val
    
    def get_owner_by_assetid(self, id):
        for i in self.asset_list:
            if i.board_loc == id:
                return i.owner
        return -1    
    
    def set_owner_to_asset(self, assetid, playerid ):
        for i in self.asset_list:
            if i.board_loc == assetid:
                i.owner = playerid
    
    def get_buyprice_by_assetid(self, id):
        for i in self.asset_list:
            if i.board_loc == id:
                return i.buy_price
        return -1     
    
    def get_players_countries(self, playerid):
        count = 0
        for i in self.asset_list:
            if i.issite():
                if i.owner == playerid or i.owner == playerid + 10:
                    count += 1
        return count                 
        
    def get_current_rent_by_assetid(self, id):
        asset = None
        for i in self.asset_list:
            if i.board_loc == id:
                if i.owner > 10:
                    return -1
                elif i.owner == 0:
                    return -1
                else:
                    asset = i  
        if asset == None:
            return -1              
        if asset.issite():
            if asset.prop_count == 0:
                color_count = 0
                for i in self.asset_list:
                    if i.issite():
                        if i.owner == asset.owner and i.color_grp == asset.color_grp:
                            color_count += 1
                if color_count >= 3:
                    return asset.current_rent * 2 
            return asset.current_rent
        else:
            grp_count = 0
            for i in self.asset_list:
                if i.isutil():
                    if i.owner == asset.owner and i.pair_grp == asset.pair_grp:
                        grp_count += 1 
            if grp_count == 2:
                return asset.pair_rent
            return asset.current_rent             
                    
    def group_wise_asset_list(self, player_id):
        redProperty = ""
        greenProperty = ""
        blueProperty = ""
        yellowProperty = ""
        utilityProperty = ""
        rc, gc, bc, yc, uc = 0, 0, 0, 0, 0
        out = ""
        for i in self.asset_list:
            if i.owner == player_id:
                if i.issite():
                    if i.color_grp == 1:
                        redProperty += i.get_name_with_prop_flag() + ","
                        rc += 1
                    elif i.color_grp == 2:
                        greenProperty += i.get_name_with_prop_flag() + ","
                        gc += 1
                    elif i.color_grp == 3:
                        blueProperty += i.get_name_with_prop_flag() + ","
                        bc += 1
                    else:
                        yellowProperty += i.get_name_with_prop_flag() + ","
                        yc += 1
                else:
                    utilityProperty += i.name + ","
                    uc += 1
            if i.owner == player_id + 10:
                if i.isSite():
                    if i.color_grp == 1:
                        redProperty += i.get_name_with_prop_flag() + "(m),"
                        rc += 1
                    elif i.color_grp == 2:
                        greenProperty += i.get_name_with_prop_flag() + "(m),"
                        gc += 1
                    elif i.color_grp == 3:
                        blueProperty += i.get_name_with_prop_flag() + "(m),"
                        bc += 1
                    else:
                        yellowProperty += i.get_name_with_prop_flag() + "(m),"
                        yc += 1
                else:
                    utilityProperty += i.name + "(m),"
                    uc += 1
        if redProperty != "":
            out += "R:%s" % redProperty
        if greenProperty != "":
            out += "G:%s" % greenProperty
        if blueProperty != "":
            out += "B:%s" % blueProperty
        if yellowProperty != "":
            out += "Y:%s" % yellowProperty
        if utilityProperty != "":
            out += "U:%s" % utilityProperty
        out = "R:%d, G:%d, B:%d, Y:%d, U:%d ##" % (rc, gc, bc, yc, uc) + out
        return out   
    
    # 1. Rent payment ()
    # 2. Country Purchase (board_location)
    # 3. Utility Purchase (board_location)
    # 4. UNO Payment (diceVal)
    # 5. Chance Payment (diceVal)
    # 6. Jail Payment ()
    # 7. Property Purchase (board_location)
    # 8. Country Mortgage (board_location)
    # 9. Utility Mortgage (board_location)
    # 10. Property Sell (board_location)
    # 11. General Payment from bank to player (amount)
    # 12. Bank cash reserve add (amount)
    # 13. Crossover Payment (amount)
    # 14. Fine Payment (amount)
    # 15. Custom Duty ()
    # 16. Travelling Duty ()
        
    def process_request(self, transaction):
        payee_acc_id = transaction.payee
        recep_acc_id = transaction.recipient 
        data = transaction.detail
        if transaction.type in [11, 13, 14]:
            if self.accounts[payee_acc_id].isenoughbalance(data):
                self.accounts[payee_acc_id].withdraw(data)
                self.accounts[recep_acc_id].deposit(data)
                self.statement_populate(0, transaction, data)
                self.statement_populate(1, transaction, data)
                return True
            return False                
        if transaction.type == 12:
            self.accounts[recep_acc_id].deposit(data)
            self.statement_populate(1, transaction, data)
            return True  
        if transaction.type in [2, 3]:
            if self.accounts[payee_acc_id].isenoughbalance(self.get_buyprice_by_assetid(data)):
                self.accounts[payee_acc_id].withdraw(self.get_buyprice_by_assetid(data))
                self.accounts[recep_acc_id].deposit(self.get_buyprice_by_assetid(data))
                self.statement_populate(0, transaction, self.get_buyprice_by_assetid(data))
                self.statement_populate(1, transaction, self.get_buyprice_by_assetid(data))       
                return True         
            else:
                return False
        if transaction.type == 1:
            if self.accounts[payee_acc_id].isenoughbalance(self.get_current_rent_by_assetid(data)):
                self.accounts[payee_acc_id].withdraw(self.get_current_rent_by_assetid(data))
                self.accounts[recep_acc_id].deposit(self.get_current_rent_by_assetid(data))
                self.statement_populate(0, transaction, self.get_current_rent_by_assetid(data))
                self.statement_populate(1, transaction, self.get_current_rent_by_assetid(data))       
                return True         
            else:
                return False
        if transaction.type == 15:
            customduty = self.get_players_countries(payee_acc_id) * 100
            if customduty > 1000:
                customduty = 1000
            if self.accounts[payee_acc_id].isenoughbalance(customduty):
                self.accounts[payee_acc_id].withdraw(customduty)
                self.accounts[recep_acc_id].deposit(customduty)
                self.statement_populate(0, transaction, customduty)
                self.statement_populate(1, transaction, customduty)
                return True
            return False  
                
        if transaction.type == 16:
            travelduty = self.get_players_countries(payee_acc_id) * 50
            if travelduty > 500:
                travelduty = 500
            if self.accounts[payee_acc_id].isenoughbalance(travelduty):
                self.accounts[payee_acc_id].withdraw(travelduty)
                self.accounts[recep_acc_id].deposit(travelduty)
                self.statement_populate(0, transaction, travelduty)
                self.statement_populate(1, transaction, travelduty)
                return True
            return False 
        
        if transaction.type == 5:
            if data == 7:
                amount = self.get_players_countries(recep_acc_id) * 100
                for i in self.accounts:
                    if i.id != recep_acc_id:
                        if i.isenoughbalance(amount):
                            i.withdraw(amount)
                            self.accounts[recep_acc_id].deposit(amount)
                            self.statement_populate(0, Transaction(i.id, recep_acc_id, 0, 0, transaction.msg), amount)
                            self.statement_populate(1, Transaction(i.id, recep_acc_id, 0, 0, transaction.msg), amount)
            
    def statement_populate(self, trans_type, trans_data, amount):
        if trans_type == 0:
            msg = trans_data.msg + ' to ' + self.accounts[trans_data.recipient].name
            statement = "{: >60} {: >8} {: >8} {: >8}".format(msg, amount, "", self.accounts[trans_data.payee].balance)
            self.accounts[trans_data.payee].transaction_statement.file_only_printer(statement)
        else:
            msg = trans_data.msg + ' from ' + self.accounts[trans_data.payee].name
            statement = "{: >60} {: >8} {: >8} {: >8}".format(msg, "", amount, self.accounts[trans_data.recipient].balance)
            self.accounts[trans_data.recipient].transaction_statement.file_only_printer(statement)        
            
        
        
        
        
        