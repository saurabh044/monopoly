from Printer import Printer


class Player(object):

    def __init__(self, logPath, player_name="", player_id=0):
        self.player_name = player_name
        self.player_id = player_id
        self.player_balance = 0
        self.logObj = Printer(logPath)
        self.player_board_position = 1
        self.asset_list = []
        self.mortgaged_assets = []
        self.asset_group_counter = {1: 0, 2: 0, 3: 0, 4: 0}
        self.util_group_flag = {1: 0, 2: 0, 3: 0}  # 1: Waterway+Satellite, 2: Railways+Roadways, 3: Airways+Petroleum
        self.transaction_statement = Printer()

    def set_player_name(self, name):
        self.player_name = name

    def set_statement_filename(self, fname):
        self.transaction_statement.set_log_file_name(fname)
        self.transaction_statement.file_only_printer("{: >60} {: >8} {: >8} {: >8}".format("Transaction Details",
                                                                                           "Debit", "Credit", "Balance"))

    def set_player_id(self, id):
        self.player_id = id

    def pay_to_me(self, amount, transaction_desc):
        self.player_balance += amount
        statement = "{: >60} {: >8} {: >8} {: >8}".format(transaction_desc, "", amount, self.getPlayerCashBalance())
        self.transaction_statement.file_only_printer(statement)

    def get_from_me(self, amount, transaction_desc):
        self.player_balance -= amount
        statement = "{: >60} {: >8} {: >8} {: >8}".format(transaction_desc, amount, "", self.getPlayerCashBalance())
        self.transaction_statement.file_only_printer(statement)

    def get_player_bank_loan_limit(self):
        bank_loan_limit = 0
        for i in self.asset_list:
            bank_loan_limit += i.get_mortgage_val()
        return bank_loan_limit

    def get_player_buildings_sell_value(self):
        value = 0
        for i in self.asset_list:
            if i.isSite():
                if i.get_property_count > 0:
                    value += (i.get_building_price() * i.get_property_count()) / 2
        return value

    def get_player_credit_available(self):
        return self.get_player_bank_loan_limit() + self.get_player_buildings_sell_value()

    def check_presence_by_board_position(self, board_pos):
        if board_pos == self.getPlayerPosition():
            return True
        else:
            return False

    def add_property_on_country(self, asset_index):
        if len(self.mortgaged_assets) == 0:
            if self.asset_group_counter[self.asset_list[asset_index].get_group()] > 2:
                if self.is_eligible_to_raise_bldg_basis_count_by_index(asset_index):
                    result = self.asset_list[asset_index].add_one_property()
                    assetname = self.asset_list[asset_index].get_name()
                    if result > 0:
                        if 1 <= result <= 3:
                            self.logObj.printer("Now there are %d houses on %s." % (result, assetname))
                        else:
                            self.logObj.printer("Now there is a hotel on %s." % assetname)
                        return True
                    else:
                        self.logObj.printer("There is already a hotel on %s. No more property can be added." % assetname)
                        return False
                else:
                    self.logObj.printer("You can't raise any building on %s till all the site of %s color have %d buildings"
                                        % (self.asset_list[asset_index].get_name(),
                                           self.asset_list[asset_index].get_group_color_name(), self.asset_list[asset_index].get_property_count()))
            else:
                self.logObj.printer("To build property, you should have at least three countries of the same color group.")
                return False
        else:
            self.logObj.printer("There are already mortgaged properties (%s). First redeem them." % self.getPlayerMortgagedRealEstateShort())
            return False

    def remove_property_of_country(self, asset_index):
        if self.is_eligible_to_destroy_bldg_basis_count_by_index(asset_index):
            result = self.asset_list[asset_index].reduce_one_property()
            assetname = self.asset_list[asset_index].get_name()
            if result < 4:
                if 1 <= result <= 3:
                    self.logObj.printer("Now there are %d houses on %s" % (result, assetname))
                else:
                    self.logObj.printer("No property left on %s." % assetname)
                return True
            else:
                self.logObj.printer("No property were there on %s." % assetname)
                return False
        else:
            return False



    def move_me(self, steps):
        self.player_board_position += steps
        if self.player_board_position > 36:
            self.logObj.printer("Hi %s, you are eligible to receive $1500 from bank." % self.player_name)
            self.player_board_position = self.player_board_position % 36
            return True
        else:
            return False

    def jump_me(self, pos):
        self.player_board_position = pos

    def __str__(self):
        return "Player ID: %d\nPlayer Name: %s\nPlayer Balance: %s\n" % (self.player_id, self.player_name, self.player_balance)

    def getPlayerPosition(self):
        return self.player_board_position

    def getPlayerName(self):
        return self.player_name

    def getPlayerID(self):
        return self.player_id

    def getPlayerCashBalance(self):
        return self.player_balance

    def getPlayerRealEstateShort(self):
        reName = self.getPlayerMortgagedRealEstateShort()
        for i in self.asset_list:
            prop_cnt = i.get_property_count()
            if 1 <= prop_cnt <= 3:
                prefix = "(h" + str(prop_cnt) + ")"
            elif prop_cnt == 4:
                prefix = "(ht)"
            else:
                prefix = ""
            reName = i.get_name() + prefix + "," + reName
        return reName

    def getPlayerMortgagedRealEstateShort(self):
        reName = ""
        for i in self.mortgaged_assets:
            reName += i.get_name() + "(m),"
        return reName

    def getPlayerAssetList(self):
        return self.asset_list

    def getPlayerAssetWithoutAnyBuildingList(self):
        asset_list = []
        asset_index = 0
        for i in self.asset_list:
            if i.isSite():
                if i.get_property_count() == 0:
                    asset_list.append((i, asset_index))
            else:
                asset_list.append((i, asset_index))
            asset_index += 1
        return asset_list

    def getPlayerAssetWithBuildingList(self):
        asset_list = []
        asset_index = 0
        for i in self.asset_list:
            if i.isSite():
                if i.get_property_count() > 0:
                    asset_list.append((i, asset_index))
            asset_index += 1
        return asset_list

    def minimum_property_price_in_all_colors_if_more_than_3(self):
        min_price = 2500
        for i in self.asset_group_counter:
            if self.asset_group_counter[i] > 2:
                min_price = min(min_price, self.minimum_property_price_by_color(i))
        return min_price

    def minimum_property_price_by_color(self, color_id):
        if color_id == 1:
            return 2000
        elif color_id == 2:
            return 1500
        else:
            return 2500

    def is_eligible_to_raise_bldg_basis_count_by_index(self, asset_index):
        if self.asset_list[asset_index].isSite():
            asset_group = self.asset_list[asset_index].get_group()
            asset_bld_cnt = self.asset_list[asset_index].get_property_count()
            group_list = []
            for i in self.asset_list:
                if i.isSite():
                    if i != asset_index:
                        if i.get_group() == asset_group:
                            group_list.append(i.get_property_count())
            if asset_bld_cnt <= min(group_list):
                return True
            else:
                return False
        else:
            return False

    def is_eligible_to_destroy_bldg_basis_count_by_index(self, asset_index):
        if self.asset_list[asset_index].isSite():
            asset_group = self.asset_list[asset_index].get_group()
            asset_bld_cnt = self.asset_list[asset_index].get_property_count()
            group_list = []
            for i in self.asset_list:
                if i.isSite():
                    if i != asset_index:
                        if i.get_group() == asset_group:
                            group_list.append(i.get_property_count())
            if asset_bld_cnt >= max(group_list):
                return True
            else:
                self.logObj.printer("Error: You can not sell property of %s till any of the country of %s color group you own have %d buildings" % (self.asset_list[asset_index].get_name(), self.asset_list[asset_index].get_group_color_name(), (asset_bld_cnt + 1) ))
                return False
        else:
            self.logObj.printer("Error: You are trying to sell building of a Utility.")
            return False


    def getSitesIndices(self):
        out = []
        if self.getPlayerCashBalance() > self.minimum_property_price_in_all_colors_if_more_than_3():
            for i in range(len(self.asset_list)):
                if self.asset_list[i].isSite():
                    if self.asset_group_counter[self.asset_list[i].get_group()] > 2:
                        if self.asset_list[i].get_property_count() != 4:
                            if self.getPlayerCashBalance() > self.asset_list[i].get_building_price():
                                out.append(i)
        else:
            self.logObj.printer("Cash is not sufficient($%d) to build any property on eligible sites (minimum required = $%d)." % (self.getPlayerCashBalance(), self.minimum_property_price_in_all_colors_if_more_than_3()))
        return out

    def isAnyPropertyMortgaged(self):
        if len(self.mortgaged_assets) > 0:
            return True
        else:
            return False

    def get_cheapest_redeemable_mortgaged_property(self):
        if self.isAnyPropertyMortgaged():
            price = self.get_asset_mortgage_value_from_mortgage_asset_index(0) * 1.1
            for i in self.mortgaged_assets:
                if (i.get_mortgage_val() * 1.1) < price:
                    price = i.get_mortgage_val() * 1.1
            return price
        else:
            return -1

    def get_cheapest_redeemable_mortgaged_property_name(self):
        if self.isAnyPropertyMortgaged():
            price = self.get_asset_mortgage_value_from_mortgage_asset_index(0)
            name = self.get_asset_mortgage_name_from_mortgage_asset_index(0)
            for i in self.mortgaged_assets:
                if i.get_mortgage_val() < price:
                    price = i.get_mortgage_val()
                    name = i.get_name()
            return name
        else:
            return ""

    def get_cost_to_redeem_all_mortgaged_properties(self):
        price = 0
        for i in self.mortgaged_assets:
            price += i.get_mortgage_val()
        return price

    def getPlayerMortgagedAssetList(self):
        return self.mortgaged_assets

    def remove_asset_from_asset_list(self, index):
        del self.asset_list[index]

    def remove_asset_from_mortgaged_list(self, index):
        del self.mortgaged_assets[index]

    def put_asset_in_mortgage_list(self, index):
        self.mortgaged_assets.append(self.asset_list[index])
        self.remove_asset_from_asset_list(index)

    def get_mortgaged_asset_in_asset_list(self, index):
        self.asset_list.append(self.mortgaged_assets[index])
        self.remove_asset_from_mortgaged_list(index)

    def get_asset_mortgage_value_from_asset_index(self, index):
        return self.asset_list[index].get_mortgage_val()

    def get_asset_mortgage_value_from_mortgage_asset_index(self, index):
        return self.mortgaged_assets[index].get_mortgage_val() * 1.1

    def get_asset_mortgage_name_from_mortgage_asset_index(self, index):
        return self.mortgaged_assets[index].get_name()

    def get_building_selling_price_from_asset_index(self, index):
        return self.asset_list[index].get_building_selling_price()

    def get_assetObj_from_index(self, index):
        return self.asset_list[index]

    def get_mortassetObj_from_index(self, index):
        return self.mortgaged_assets[index]

    def get_asset_name_from_index(self, index):
        return self.asset_list[index].get_name()

    def get_mort_asset_name_from_index(self, index):
        return self.mortgaged_assets[index].get_name()

    def player_assets_valuation(self):
        total_value = 0
        for i in self.asset_list:
            total_value += i.getBuyPrice()
        total_value += self.getPlayerCashBalance()
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
                    redProperty += i.get_name_with_prop_flag() + ","
                elif i.get_group() == 2:
                    greenProperty += i.get_name_with_prop_flag() + ","
                elif i.get_group() == 3:
                    blueProperty += i.get_name_with_prop_flag() + ","
                else:
                    yellowProperty += i.get_name_with_prop_flag() + ","
            else:
                utilityProperty += i.get_name() + ","
        for i in self.mortgaged_assets:
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

    def print_player_assets(self):
        self.logObj.printer("Player ID: %d\nPlayer Name: %s\nPlayer Cash: %s\nPlayer Assets: %s\n" % (self.player_id,
                                                                                         self.player_name,
                                                                                         self.player_balance,
                                                                                         self.getPlayerRealEstateShort()))
