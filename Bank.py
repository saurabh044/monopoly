from Printer import Printer

class Bank(object):

    def __init__(self, banker_name, bank_id=5):
        self.banker_name = banker_name
        self.initial_money = 0        
        self.bank_id = bank_id
        self.balance = 0
        self.asset_list = []
        self.mortgage_ownership = []
        
        self.transaction_statement = Printer()
        self.asset_group_counter = {1: 0, 2: 0, 3: 0, 4: 0}
        self.transaction_statement.set_log_file_name("./game_logs/bank_transactions_statement.txt")
        self.transaction_statement.file_only_printer("{: >60} {: >8} {: >8} {: >8}".format("Transaction Details",
                                                                                           "Debit", "Credit", "Balance"))

    def set_bank_initial_money(self, amount, transaction_desc):
        self.initial_money = amount
        self.balance = amount

    def pay_to_me(self, amount, transaction_desc):
        self.balance += amount
        statement = "{: >60} {: >8} {: >8} {: >8}".format(transaction_desc, "", amount, self.getBankCashBalance())
        self.transaction_statement.file_only_printer(statement)

    def get_from_me(self, amount, transaction_desc):
        self.balance -= amount
        statement = "{: >60} {: >8} {: >8} {: >8}".format(transaction_desc, amount, "", self.getBankCashBalance())
        self.transaction_statement.file_only_printer(statement)

    def getbankerName(self):
        return self.banker_name

    def getBankID(self):
        return self.bank_id

    def getBankCashBalance(self):
        return self.balance

    def getBankRealEstateShort(self):
        reName = self.getBankMortgageRealEstateShort()
        for i in self.asset_list:
            reName = i.get_name() + "," + reName
        return reName

    def getBankMortgageRealEstateShort(self):
        reName = ""

        for i in self.mortgage_ownership:
            reName += i.get_name() + "(M" + str(i.get_ownership()-10) + "),"
        return reName

    def addAssetinMortgageListFromPlayers(self,assetObj):
        self.mortgage_ownership.append(assetObj)

    def removeAssetfromMortgageList(self, assetObj):
        self.mortgage_ownership.remove(assetObj)

    def bank_assets_valuation(self):
        total_value = 0
        for i in self.asset_list:
            total_value += i.getBuyPrice()
        for i in self.mortgage_ownership:
            total_value += i.getBuyPrice()
        total_value += self.getBankCashBalance()
        return total_value

    def group_wise_asset_list(self):
        redProperty = ""
        greenProperty = ""  
        blueProperty = ""   
        yellowProperty = ""
        utilityProperty = ""
        out = ""
        for i in self.asset_list:
            if i.isSite():
                if i.get_group() == 1:
                    redProperty += i.get_name() + ","
                elif i.get_group() == 2:
                    greenProperty += i.get_name() + ","
                elif i.get_group() == 3:
                    blueProperty += i.get_name() + ","
                else:
                    yellowProperty += i.get_name() + ","
            else:
                utilityProperty += i.get_name() + ","
        for i in self.mortgage_ownership:
            if i.isSite():
                if i.get_group() == 1:
                    redProperty += i.get_name() + "(m),"
                elif i.get_group() == 2:
                    greenProperty += i.get_name() + "(m),"
                elif i.get_group() == 3:
                    blueProperty += i.get_name() + "(m),"
                else:
                    yellowProperty += i.get_name() + "(m),"
            else:
                utilityProperty += i.get_name() + "(m),"
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
        out = "R:%d, G:%d, B:%d, Y:%d ##" % (self.asset_group_counter[1], self.asset_group_counter[2],
                                            self.asset_group_counter[3], self.asset_group_counter[4]) + out
        return out
