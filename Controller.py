from Player import Player
from Country import Country
from Utility import Utility
from Bank import Bank
from MenuBox import MenuBox
from MenuBox2 import MenuBox2
import re
from Printer import Printer


class Controller(object):

    def __init__(self, player_count, log_path):
        self.name = "Game Controller"
        self.logObj = Printer(log_path)
        self.playerCount = player_count
        self.playersName = []
        self.turnHolderPlayerID = 0
        self.BoardData = {}
        self.gameState = 0
        self.logPath = log_path
        self.available_players_in_game = []
        self.available_players_index = {}
        for i in range(36):
            self.BoardData[i+1] = []
        self.Players = []
        self.country_name_list = ["England", "Iraq", "France", "Iran", "Egypt", "Canada", "Germany", "Swiss", "Brazil",
                                  "Italy", "Japan", "USA", "Mexico", "Hongkong", "Australia", "India", "SaudiArab",
                                  "China", "Malaysia", "Singapore"]
        # key value array of Utility [boardPosition, buyValue, mortgageValue]
        self.utility_name_list = ["Waterways", "Satellite", "Airways", "Roadways", "Petroleum", "Railways"]
        self.country_objs = []
        self.utility_objs = []
        self.country_util_name_id_dict = {}
        self.Banker = Bank("SBI")
        self.Banker.set_bank_initial_money(1000000, "Initialised the bank cash reserve with $1000000.")
        self.properties_board_locations = {2: "",  3: "",  4: "",  6: "",
                                           7: "",  8: "",  9: "", 11: "",
                                           12: "", 13: "", 15: "", 16: "",
                                           18: "", 20: "", 21: "", 23: "",
                                           24: "", 25: "", 27: "", 29: "",
                                           31: "", 32: "", 33: "", 34: "",
                                           35: "", 36: ""}
        self.board_display_data = ["Start", "England R($2500)#", "Iraq G($5000)+", "Waterways U($9500)", "UNO",
                                   "France R($2500)#", "Iran G($2500)+", "Satellite U($2000)", "Egypt G($3200)+",
                                   "Resort", "Canada Y($4000)%", "Germany R($3500)#", "Airways U($10500)",
                                   "Custom Duty", "Swiss R($3500)#", "Brazil Y($2500)%",
                                   "Chance", "Italy R($3500)#", "Party House", "Japan B($2500)^",
                                   "USA Y($8500)%", "Travelling Duty", "Roadways U($3500)", "Mexico Y($4000)%",
                                   "Hongkong B($2000)^", "UNO", "Australia Y($3300)%", "Jail",
                                   "India B($5500)^", "Chance", "SaudiArab G($5500)+", "Petroleum U($5500)",
                                   "China B($4500)^", "Railways U($9500)", "Malaysia G($1500)+", "Singapore B($3000)^"]

        for i in range(self.playerCount):
            self.Players.append(Player(self.logPath))
            self.available_players_in_game.append(i+1)
            self.available_players_index[i+1] = i

    def get_players_name(self):
        i = 0
        while i < len(self.Players):
            inp = raw_input("Enter name for Player-%d : " % (i+1))
            self.playersName.append(inp)
            i += 1

    def add_players_in_game(self):
        i = 0
        while i < len(self.Players):
            self.Players[i].set_player_id(i+1)
            self.Players[i].set_player_name(self.playersName[i])
            self.Players[i].set_statement_filename("./game_logs/Player-%d_account_statement.txt" % (i+1))
            i += 1

    def give_initial_money_to_player(self):
        for i in range(len(self.Players)):
            self.payment_channel(self.Players[i].getPlayerID(), 5, 25000, "Game Initial Money")

    def assign_all_assets_to_bank_initially(self):
        for i in self.country_objs:
            self.Banker.asset_list.append(i)
            self.Banker.asset_group_counter[i.get_group()] += 1
        for i in self.utility_objs:
            self.Banker.asset_list.append(i)

    def add_countries_in_game(self):
        # key value array of country [boardPosition, buyValue, mortgageValue, colorGroup, basicRent, property_price, property_rent]
        country_list = {"England":   [ 2, 2500, 3500, 1, 700, 7000, 1700],
                        "Iraq":      [ 3, 5000, 2500, 2, 500, 5000, 1500],
                        "France":    [ 6, 2500, 1250, 1, 300, 2500, 1300],
                        "Iran":      [ 7, 2500, 1250, 2, 300, 2500, 1300],
                        "Egypt":     [ 9, 3200, 1500, 2, 300, 3200, 1300],
                        "Canada":    [11, 4000, 2000, 4, 400, 4000, 1400],
                        "Germany":   [12, 3500, 1750, 1, 400, 3500, 1400],
                        "Swiss":     [15, 3500, 3300, 1, 700, 6500, 1700],
                        "Brazil":    [16, 2500, 1300, 4, 300, 2500, 1300],
                        "Italy":     [18, 3500, 1000, 1, 200, 2000, 1200],
                        "Japan":     [20, 2500, 1250, 3, 250, 2500, 1250],
                        "USA":       [21, 8500, 5000, 4, 1000, 8500, 2000],
                        "Mexico":    [24, 4000, 2000, 4, 900, 4000, 1800],
                        "Hongkong":  [25, 2000, 1000, 3, 200, 2500, 1200],
                        "Australia": [27, 3300, 2000, 4, 400, 3300, 1400],
                        "India":     [29, 5500, 2750, 3, 550, 5500, 1550],
                        "SaudiArab": [31, 5500, 2800, 2, 600, 5500, 1600],
                        "China":     [33, 4500, 2250, 3, 450, 4500, 1450],
                        "Malaysia":  [35, 1500,  800, 2, 200, 1500, 1200],
                        "Singapore": [36, 3000, 1500, 3, 300, 3000, 1300]
                        }
        # key value array of Utility [boardPosition, buyValue, mortgageValue]
        utility_list = {"Waterways": [4, 9500, 2000, 1400, 2200],
                        "Satellite": [8, 2000, 1250, 500, 1000],
                        "Airways": [13, 10500, 5500, 1500, 2500],
                        "Roadways": [23, 3500, 1800, 800, 1500],
                        "Petroleum": [32, 5500, 1300, 500, 1000],
                        "Railways": [34, 9500, 5000, 1500, 2500]
                        }
        country_cnt = 0
        util_cnt = 0
        for i in country_list:
            self.country_objs.append(Country(country_list[i][3], country_list[i][0], i, country_list[i][1], country_list[i][2], country_list[i][4], country_list[i][5], country_list[i][6]))
            self.country_util_name_id_dict[i] = country_cnt
            country_cnt += 1
        for i in utility_list:
            self.utility_objs.append(Utility(utility_list[i][0], i, utility_list[i][1], utility_list[i][2], utility_list[i][3], utility_list[i][4]))
            self.country_util_name_id_dict[i] = util_cnt
            util_cnt += 1
        for i in range(6):
            if self.utility_objs[i].get_name() == "Waterways" or self.utility_objs[i].get_name() == "Satellite":
                self.utility_objs[i].set_util_group(1)
            elif self.utility_objs[i].get_name() == "Railways" or self.utility_objs[i].get_name() == "Roadways":
                self.utility_objs[i].set_util_group(2)
            else:
                self.utility_objs[i].set_util_group(3)
        self.assign_all_assets_to_bank_initially()

    def find_if_name_is_country_or_util(self, name):  # it will return 1 for country, 2 for utility and 0 if not found.
        if name in self.country_name_list:
            return 1
        elif name in self.utility_name_list:
            return 2
        else:
            return 0

    def print_player_details(self):
        i = 0
        while i < len(self.Players):
            self.logObj.printer(self.Players[i])
            i += 1

    def print_country_details(self):
        i = 0
        while i < len(self.country_objs):
            self.logObj.printer(self.country_objs[i])
            i += 1
        i = 0
        while i < len(self.utility_objs):
            self.logObj.printer(self.utility_objs[i])
            i += 1

    def remove_player_from_game(self, player_id):
        self.payment_channel(5, player_id, self.get_player_by_its_ID(player_id).getPlayerCashBalance(), "Surrender money" )
        self.surrender_all_assets_to_bank(player_id)
        if self.available_players_in_game > 2:
            if self.get_turnHolderPlayerID() == player_id:
                indx = self.available_players_in_game.index(player_id)-1
                self.set_turnHolderPlayerID(self.available_players_in_game[indx])
        for i in self.available_players_in_game:
            if i > player_id:
                self.available_players_index[i] -= 1
        self.Players.remove(self.get_player_by_its_ID(player_id))
        self.available_players_in_game.remove(player_id)
        del self.available_players_index[player_id]

    def get_players_position(self):
        positions = []
        i = 0
        while i < len(self.Players):
            positions.append(self.Players[i].getPlayerPosition())
            i += 1
        return positions

    def set_turnHolderPlayerID(self, pl_id):
        self.turnHolderPlayerID = pl_id

    def move_turnHolderPlayerID(self):
        self.turnHolderPlayerID = self.available_players_in_game[(self.available_players_in_game.index(self.get_turnHolderPlayerID()) + 1) % len(self.available_players_in_game)]

    def get_turnHolderPlayerID(self):
        return self.turnHolderPlayerID

    def get_player_by_its_ID(self, ids):
        if ids == 5:
            return self.Banker
        else:
            return self.Players[self.available_players_index[ids]]

    def get_player_cash_balance(self, ids):
        return self.Players[self.available_players_index[ids]].getPlayerCashBalance()

    def get_player_name_by_its_ID(self, ids):
        return self.Players[self.available_players_index[ids]].getPlayerName()

    def print_all_player_assets_table(self):
        total_cash_reserver = 0
        total_asset_reserver = 0
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format("PID", "Name", "Cash", "NetWorth", "Assets"))
        for i in range(len(self.Players)):
            total_cash_reserver += self.Players[i].getPlayerCashBalance()
            total_asset_reserver += self.Players[i].player_assets_valuation()
            self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format(self.Players[i].getPlayerID(), self.Players[i].getPlayerName()
                                                   , self.Players[i].getPlayerCashBalance(), self.Players[i].player_assets_valuation(),
                                                   self.Players[i].group_wise_asset_list()))
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format("BID", "Name", "Cash", "NetWorth", "Assets"))
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format(self.Banker.getBankID(),
                                                                           self.Banker.getbankerName(),
                                                                           self.Banker.getBankCashBalance(),
                                                                           self.Banker.bank_assets_valuation(),
                                                                           self.Banker.group_wise_asset_list()))
        total_cash_reserver += self.Banker.getBankCashBalance()
        total_asset_reserver += self.Banker.bank_assets_valuation()
        if total_cash_reserver != 1000000:
            self.logObj.printer("Cash-Balance issue occurred.")
        if total_asset_reserver != 1113500:
            self.logObj.printer("Asset-Balance issue occurred.")
        self.logObj.printer("")

    def countryPriceByName(self, name):
        country_index = self.country_util_name_id_dict[name]
        return self.country_objs[country_index].getBuyPrice()

    def UtilPriceByName(self, name):
        util_index = self.country_util_name_id_dict[name]
        return self.utility_objs[util_index].getBuyPrice()

    def display_board(self):
        i = 0
        while i < len(self.board_display_data):
            pp = self.check_all_player_presence_on_a_position(i+1)
            if (i+1) in self.properties_board_locations:
                owner_tag = self.properties_board_locations[i+1]
            else:
                owner_tag = ""
            loc = ""
            for j in range(len(pp)):
                if pp[j]:
                    loc = loc + "<P" + str(self.available_players_in_game[j]) + ">"
            self.BoardData[i+1] = [self.board_display_data[i], owner_tag, loc]
            i += 1
        self.logObj.printer("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(9):
            self.logObj.printer("{: >20} {: <6} {: <16} {: >20} {: <6} {: <16} {: >20} {: <6} {: <16} {: >20} {: <6} {: <16}".format(
                                                           self.BoardData[i + 1][0],
                                                           self.BoardData[i + 1][1],
                                                           self.BoardData[i + 1][2],
                                                           self.BoardData[i + 10][0],
                                                           self.BoardData[i + 10][1],
                                                           self.BoardData[i + 10][2],
                                                           self.BoardData[i + 19][0],
                                                           self.BoardData[i + 19][1],
                                                           self.BoardData[i + 19][2],
                                                           self.BoardData[i + 28][0],
                                                           self.BoardData[i + 28][1],
                                                           self.BoardData[i + 28][2],
                                                           ))
        self.logObj.printer("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

    def get_country_util_by_board_position(self, board_pos):
        board_pos_val = self.board_display_data[board_pos-1]
        matchObj = re.search(r'(.+)\s.*([RGYBU])\(\$', board_pos_val, re.M | re.I)
        if matchObj is not None:
            board_country_util_name = matchObj.group(1)
            if matchObj.group(2) == 'U':
                return self.utility_objs[self.country_util_name_id_dict[board_country_util_name]]
            else:
                return self.country_objs[self.country_util_name_id_dict[board_country_util_name]]
        else:
            return None

    def sell_property_to_player(self, PlayerID):
        board_pos = self.get_player_by_its_ID(PlayerID).getPlayerPosition()
        if self.get_country_util_by_board_position(board_pos).get_ownership() == 0:
            country_util_obj = self.get_country_util_by_board_position(board_pos)
            self.get_player_by_its_ID(PlayerID).asset_list.append(country_util_obj)
            if country_util_obj.isSite():
                self.get_player_by_its_ID(PlayerID).asset_group_counter[country_util_obj.get_group()] += 1
            if country_util_obj.isUtil():
                self.get_player_by_its_ID(PlayerID).util_group_flag[country_util_obj.get_util_group()] += 1
            self.payment_channel(5, PlayerID, country_util_obj.getBuyPrice(), "%s sold to Player-%d" % (self.get_position_name_where_player_standing(PlayerID), PlayerID))
            self.get_country_util_by_board_position(board_pos).set_ownership(PlayerID)
            if country_util_obj.isSite():
                self.Banker.asset_group_counter[country_util_obj.get_group()] -= 1
            self.Banker.asset_list.remove(country_util_obj)
            self.properties_board_locations[board_pos] = "|P" + str(PlayerID) + "|"

        else:
            self.logObj.printer("Property already sold.")

    def check_property_availability_status(self, PlayerID):
        board_pos = self.get_player_by_its_ID(PlayerID).getPlayerPosition()
        if board_pos in self.properties_board_locations:
            if self.get_country_util_by_board_position(board_pos).get_ownership() == 0:
                return True
            else:
                return False

    def check_property_buy_price(self, PlayerID):
        board_pos = self.get_player_by_its_ID(PlayerID).getPlayerPosition()
        if board_pos in self.properties_board_locations:
            return self.get_country_util_by_board_position(board_pos).getBuyPrice()
        else:
            return 0

    def check_player_ability_to_buy_property(self, PlayerID):
        if self.check_property_buy_price(PlayerID) < self.get_player_cash_balance(PlayerID):
            return True
        else:
            return False

    def get_property_owner_where_player_standing(self, PlayerID):
        board_pos = self.get_player_by_its_ID(PlayerID).getPlayerPosition()
        if board_pos in self.properties_board_locations:
            return self.get_country_util_by_board_position(board_pos).get_ownership()
        else:
            return -1

    def get_property_rent_where_player_standing(self, PlayerID):
        board_pos = self.get_player_by_its_ID(PlayerID).getPlayerPosition()
        if board_pos in self.properties_board_locations:
            ownerID = self.get_property_owner_where_player_standing(PlayerID)
            if ownerID > 10:
                ownerID -= 10
            if self.get_country_util_by_board_position(board_pos).isSite() is True and ownerID != 0:
                prop_cnt = self.get_country_util_by_board_position(board_pos).get_property_count()
                if self.get_player_by_its_ID(ownerID).asset_group_counter[self.get_country_util_by_board_position(board_pos).get_group()] > 2 and prop_cnt == 0:
                    self.logObj.printer("Double site rent attracted.")
                    return self.get_country_util_by_board_position(board_pos).get_rent() * 2
                else:
                    return self.get_country_util_by_board_position(board_pos).get_rent()
            elif self.get_country_util_by_board_position(board_pos).isUtil() is True and ownerID != 0:
                if self.get_player_by_its_ID(ownerID).util_group_flag[self.get_country_util_by_board_position(board_pos).get_util_group()] > 1:
                    self.logObj.printer("Paired rent attracted for %s." % self.get_country_util_by_board_position(board_pos).get_name())
                    return self.get_country_util_by_board_position(board_pos).get_paired_rent()
                else:
                    return self.get_country_util_by_board_position(board_pos).get_rent()
            else:
                self.logObj.printer("Position not occupied by any player.")
                return self.get_country_util_by_board_position(board_pos).get_rent()
        else:
            return -1

    def get_position_name_where_player_standing(self, PlayerID):
        board_pos = self.get_board_position_where_player_standing(PlayerID)
        pos_name = self.board_display_data[board_pos-1]
        return pos_name

    def get_board_position_where_player_standing(self, PlayerID):
        return self.get_player_by_its_ID(PlayerID).getPlayerPosition()

    def transaction_between_two_player(self, recipient, sender, amount):
        self.payment_channel(recipient, sender, amount, "Player-%d to Player-%d" % (sender, recipient))

    def transmit_from_one_to_rest(self, sender, amount, reason_text):
        if self.check_a_player_if_negative_bal_after_deduction(sender,
                                                               amount * (len(self.available_players_in_game) - 1)):
            for i in self.available_players_in_game:
                if i != sender:
                    self.payment_channel(i, sender, amount, "Player-%d paid to all: resort." % sender)
        else:
            self.logObj.printer("Player-%d is not able to pay the amount as bankrupt and deposited all the assets/cash to bank." % sender)

    def receive_from_all_to_one(self, receiver, amount, reason_text):
        for i in self.available_players_in_game:
            if i != receiver:
                self.payment_channel(receiver, i, amount, "Receive from all: %s" % reason_text)

    def pay_fine(self, culprit, amount, reason_text):
        self.payment_channel(5, culprit, amount, reason_text)

    def receive_reward(self, recipient, amount, reason_text):
        self.payment_channel(recipient, 5, amount, reason_text)

    def get_site_count_of_player(self, player_id):
        total_sites = 0
        for i in range(len(self.get_player_by_its_ID(player_id).asset_list)):
            if self.get_player_by_its_ID(player_id).asset_list[i].isSite():
                total_sites += 1
        return total_sites

    def payCustomDuty(self, recipient):
        total_sites = self.get_site_count_of_player(recipient)
        if total_sites > 9:
            duty = 1000
        else:
            duty = total_sites * 100
        self.logObj.printer("Payment required for custom duty of $%d." % duty)
        self.payment_channel(5, recipient, duty, "Custom Duty")

    def payTravellingDuty(self, recipient):
        total_sites = self.get_site_count_of_player(recipient)
        if total_sites > 9:
            duty = 500
        else:
            duty = total_sites * 50
        self.logObj.printer("Payment required for travelling duty of $%d." % duty)
        self.payment_channel(5, recipient, duty, "travelling Duty")

    def enjoyment_in_resort(self, player_id):
        self.transmit_from_one_to_rest(player_id, 200, "Resort money")

    def get_party_from_others(self, player_id):
        self.receive_from_all_to_one(player_id, 200, "Reached party house")

    def gotojail(self,player_id):
        if self.check_a_player_if_negative_bal_after_deduction(player_id, 100):
            self.pay_fine(player_id, 100, "Reached on Jail")
        else:
            self.logObj.printer("Player-%d is not able to pay the amount as bankrupt and deposited all the assets/cash to bank." % player_id)

    def check_all_player_presence_on_a_position(self, board_pos):
        pres = []
        for i in self.Players:
            pres.append(i.check_presence_by_board_position(board_pos))
        return pres

    def apply_uno_to_player(self, recipient, rule_num):
        if rule_num == 2:
            self.logObj.printer("It is your anniversary, collect $500 from each player.")
            self.receive_from_all_to_one(recipient, 500, "UNO-2: Anniversary gift.")
        elif rule_num == 4:
            self.logObj.printer("1st prize in Beauty Contest of $2500.")
            self.receive_reward(recipient, 2500, "UNO-4, Won Beauty Contest")
        elif rule_num == 6:
            self.logObj.printer("Income tax refund of $2000.")
            self.receive_reward(recipient, 2000, "UNO-6, IT refund")
        elif rule_num == 8:
            self.logObj.printer("Go to party house and collect $200 from each player.")
            self.receive_from_all_to_one(recipient, 200, "UNO-8: Party house")
            self.get_player_by_its_ID(recipient).jump_me(19)
        elif rule_num == 10:
            self.logObj.printer("Receive interest on shares of $1500.")
            self.receive_reward(recipient, 1500, "UNO-10: shares interest")
        elif rule_num == 12:
            self.logObj.printer("Receive amount of $3000 after sale of stocks.")
            self.receive_reward(recipient, 3000, "UNO-12: sale of stocks")
        elif rule_num == 3:
            self.logObj.printer("Go to jail.")
            self.pay_fine(recipient, 500, "UNO-3: Sent to Jail.")
            self.get_player_by_its_ID(recipient).jump_me(28)
        elif rule_num == 5:
            self.logObj.printer("School and medical fees expenses of $2500.")
            self.pay_fine(recipient, 2500, "UNO-5: School Fees.")
        elif rule_num == 7:
            self.logObj.printer("Submit your passport and pay $5000 fine.")
            self.pay_fine(recipient, 5000, "UNO-7: Passport Deposit")
        elif rule_num == 9:
            self.logObj.printer("Make general repair on your properties of $100")
            self.pay_fine(recipient, 100, "UNO-9: Repair")
        elif rule_num == 11:
            self.logObj.printer("Pay insurance premium of $1500.")
            self.pay_fine(recipient, 1500, "UNO-11, Insurance Premium")
        else:
            pass

    def apply_chance_to_player(self, recipient, rule_num):
        if rule_num == 2:
            self.logObj.printer("Loss in share market of $2000.")
            self.pay_fine(recipient, 2000, "Chance-2: Loss in share market")
        elif rule_num == 4:
            self.logObj.printer("Fine for accident due to wrong driving of $1000")
            self.pay_fine(recipient, 1000, "Chance-4: Driving fine")
        elif rule_num == 6:
            self.logObj.printer("House repair of $1500.")
            self.pay_fine(recipient, 1500, "Chance-6: House repair")
        elif rule_num == 8:
            self.logObj.printer("Loss of $3000 due to fire in Go-down.")
            self.pay_fine(recipient, 3000, "Chance-8: Loss due to fire")
        elif rule_num == 10:
            self.logObj.printer("Go to jail.")
            self.pay_fine(recipient, 500, "Chance-10: Sent to jail")
            self.get_player_by_its_ID(recipient).jump_me(28)
        elif rule_num == 12:
            self.logObj.printer("Repair of your car of $200.")
            self.pay_fine(recipient, 200, "Chance-12: Car repair")
        elif rule_num == 3:
            self.logObj.printer("Won lottery prize of $2500.")
            self.receive_reward(recipient, 2500, "Chance-3: won lottery")
        elif rule_num == 5:
            self.logObj.printer("You have won cross-word prize of $1000.")
            self.receive_reward(recipient, 1000, "Chance-5: won cross-word")
        elif rule_num == 7:
            self.logObj.printer("Collect $100 rent from each player for all of your site.")
            self.receive_from_all_to_one(recipient, 100 * self.get_site_count_of_player(recipient),
                                         "Chance-7: Rent collection")
        elif rule_num == 9:
            self.logObj.printer("You have won the jackpot of $2000.")
            self.receive_reward(recipient, 2000, "Chance-9: won jackpot")
        elif rule_num == 11:
            self.logObj.printer("Prize for best performance in export of $1500.")
            self.receive_reward(recipient, 1500, "Chance-11: Best exporter")
        else:
            pass

    def display_player_asset_list_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerAssetList()) > 0:
            assetsMenu = MenuBox("Asset List", self.logPath)
            for i in self.get_player_by_its_ID(player_id).getPlayerAssetList():
                assetsMenu.addOption(i.get_name_with_mortgage_value())
            return assetsMenu
        else:
            self.logObj.printer("No asset available for Player-%d" % player_id)
            return None

    def display_player_asset_list_without_buildings_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerAssetWithoutAnyBuildingList()) > 0:
            assetsMenu = MenuBox2("Asset list without any buildings on it", self.logPath)
            for i in self.get_player_by_its_ID(player_id).getPlayerAssetWithoutAnyBuildingList():
                assetsMenu.addOption(i[0].get_name_with_mortgage_value(), i[1])
            return assetsMenu
        else:
            self.logObj.printer("No asset without any building available for Player-%d" % player_id)
            return None

    def display_player_asset_list_with_buildings_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerAssetWithBuildingList()) > 0:
            assetsMenu = MenuBox2("Asset list with buildings", self.logPath)
            for i in self.get_player_by_its_ID(player_id).getPlayerAssetWithBuildingList():
                assetsMenu.addOption(i[0].get_name_with_single_building_sell_value(), i[1])
            return assetsMenu
        else:
            self.logObj.printer("No asset with any building available for Player-%d" % player_id)
            return None

    def display_player_raise_cash_menu(self, player_id):
        assetsMenu = MenuBox("Raise cash via", self.logPath, 0)
        assetsMenu.addOption("Mortgage Property")
        assetsMenu.addOption("Sell a Building")
        return assetsMenu

    def display_player_mortgaged_asset_list_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerMortgagedAssetList()) > 0:
            assetsMenu = MenuBox("Mortgaged Asset List", self.logPath)
            for i in self.get_player_by_its_ID(player_id).getPlayerMortgagedAssetList():
                assetsMenu.addOption(i.get_name_with_mortgage_value())
            return assetsMenu
        else:
            self.logObj.printer("No asset is mortgaged to bank for Player-%d" % player_id)
            return None

    def check_players_with_negative_cash(self):
        player_to_remove = []
        for i in self.available_players_index.values():
            if self.Players[i].getPlayerCashBalance() < 0:
                if (self.Players[i].get_player_credit_available() + self.Players[i].getPlayerCashBalance()) > 0:
                    while self.Players[i].getPlayerCashBalance() < 0:
                        assetSelectMenu = self.display_player_asset_list_menu(self.Players[i].getPlayerID())
                        if assetSelectMenu is not None:
                            optionGot = assetSelectMenu.runMenu()
                            if optionGot != assetSelectMenu.getoptioncount():
                                asset_index = optionGot - 1
                                self.change_ownership_of_country_util(self.Players[i].get_asset_name_from_index(asset_index),
                                                                      self.Players[i].getPlayerID())
                                self.payment_channel(self.Players[i].getPlayerID(), 5, self.Players[i].get_asset_mortgage_value_from_asset_index(asset_index), "mortgaged money transfer")
                                self.Banker.addAssetinMortgageListFromPlayers(self.Players[i].get_assetObj_from_index(asset_index))
                                self.Players[i].put_asset_in_mortgage_list(asset_index)
                            else:
                                self.logObj.printer("Your cash balance is negative ($%d) so can not exit. Please mortgage some assets and get some cash to remain in game." % self.Players[i].getPlayerCashBalance() )
                        else:
                            self.logObj.printer("You do not have any assets remaining with you!")
                else:
                    self.logObj.printer("Player-%d is not able to pay the amount as bankrupt and deposited all the assets/cash to bank.\nBye!!!" % self.Players[i].getPlayerID())
                    player_to_remove.append(self.Players[i])
        for i in player_to_remove:
            self.remove_player_from_game(i.getPlayerID())
        if len(self.Players) == 1:
            self.set_game_state(-1)

    def change_ownership_of_country_util(self, objName, playerID):
        objType = self.find_if_name_is_country_or_util(objName)
        if objType == 1:  # 1 for country
            self.country_objs[self.country_util_name_id_dict[objName]].set_ownership(10 + playerID)
        elif objType == 2:
            self.utility_objs[self.country_util_name_id_dict[objName]].set_ownership(10 + playerID)
        else:
            pass

    def reverse_ownership_of_country_util(self, objName, playerID):
        objType = self.find_if_name_is_country_or_util(objName)
        if objType == 1:  # 1 for country
            self.country_objs[self.country_util_name_id_dict[objName]].set_ownership(playerID)
        elif objType == 2:
            self.utility_objs[self.country_util_name_id_dict[objName]].set_ownership(playerID)
        else:
            pass

    def set_game_state(self, state):
        self.gameState = state  # only 0, 1, -1 allowed in input. 0: inactive, 1: active, -1: finished , -2: Draw

    def get_game_state(self):
        return self.gameState

    def get_winner_name(self):
        return self.Players[0].getPlayerName()

    def printing(self, inp_text):
        self.logObj.printer(inp_text)

    def check_bank_with_negative_cash(self, amount):
        if self.Banker.getBankCashBalance() < amount:
            self.logObj.printer("Bank has ran out of cash. Game Drawn.")
            self.set_game_state(-2)
            return False
        else:
            return True

    def redeem_mortgaged_property_of_player(self, player_id):
        if self.get_player_by_its_ID(player_id).isAnyPropertyMortgaged() is False:
            print "None of your property is mortgaged to bank."
        loop_flag = True
        while self.get_player_by_its_ID(player_id).isAnyPropertyMortgaged() is True and loop_flag is True:
            self.logObj.printer("Player cash balance = %d" % self.get_player_by_its_ID(player_id).getPlayerCashBalance())
            self.logObj.printer("Cheapest redeemable property %s = %d" % (self.get_player_by_its_ID(player_id).get_cheapest_redeemable_mortgaged_property_name(), self.get_player_by_its_ID(player_id).get_cheapest_redeemable_mortgaged_property()))
            if self.get_player_by_its_ID(player_id).getPlayerCashBalance() > self.get_player_by_its_ID(player_id).get_cheapest_redeemable_mortgaged_property():
                mortassetSelectMenu = self.display_player_mortgaged_asset_list_menu(player_id)
                if mortassetSelectMenu is not None:
                    optionGot = mortassetSelectMenu.runMenu()
                    if optionGot != mortassetSelectMenu.getoptioncount():
                        mortassetindex = optionGot - 1
                        mortassetname = self.get_player_by_its_ID(player_id).get_mort_asset_name_from_index(mortassetindex)
                        mortassetredeemprice = self.get_player_by_its_ID(player_id).get_asset_mortgage_value_from_mortgage_asset_index(mortassetindex)
                        if mortassetredeemprice < self.get_player_by_its_ID(player_id).getPlayerCashBalance():
                            self.reverse_ownership_of_country_util(mortassetname, player_id)
                            self.payment_channel(5, player_id, mortassetredeemprice, "Redemption of property %s" % mortassetname)
                            self.Banker.removeAssetfromMortgageList(self.get_player_by_its_ID(player_id).get_mortassetObj_from_index(mortassetindex))
                            self.get_player_by_its_ID(player_id).get_mortgaged_asset_in_asset_list(mortassetindex)
                        else:
                            self.logObj.printer("You don't have sufficient cash balance to redeem %s" % mortassetname)
                    else:
                        loop_flag = False
                else:
                    self.logObj.printer("No property is mortgaged to bank.")
                    loop_flag = False
            else:
                self.logObj.printer("Cash balance is not sufficient to redeem any other mortgaged property.")
                loop_flag = False

    def check_a_player_if_negative_bal_after_deduction(self, player_id, amount):
        if self.get_player_by_its_ID(player_id).getPlayerCashBalance() < amount:
            self.logObj.printer("Low cash balance ($%s) with Player-%d" % (self.get_player_cash_balance(player_id),
                                                                           player_id))
            if (self.get_player_by_its_ID(player_id).get_player_credit_available() + self.get_player_by_its_ID(player_id).getPlayerCashBalance()) > amount:
                self.logObj.printer("Player-%d has not enough balance to pay the amount $%s. Please mortgage/sell some of your properties to bank." % (player_id, amount))
                while self.get_player_by_its_ID(player_id).getPlayerCashBalance() < amount:
                    cashraisemethodmenu = self.display_player_raise_cash_menu(player_id)
                    optforcash = cashraisemethodmenu.runMenu()
                    if optforcash == 1:
                        assetSelectMenu = self.display_player_asset_list_without_buildings_menu(player_id)
                        if assetSelectMenu is not None:
                            optionGot = assetSelectMenu.runMenu()
                            if optionGot[0] != assetSelectMenu.getoptioncount():
                                asset_index = optionGot[1]
                                mortprice = self.get_player_by_its_ID(player_id).get_asset_mortgage_value_from_asset_index(asset_index)
                                self.change_ownership_of_country_util(self.get_player_by_its_ID(player_id).get_asset_name_from_index(asset_index), player_id)
                                self.payment_channel(player_id, 5, mortprice, "mortgaged money transfer")
                                self.Banker.addAssetinMortgageListFromPlayers(self.get_player_by_its_ID(player_id).get_assetObj_from_index(asset_index))
                                self.get_player_by_its_ID(player_id).put_asset_in_mortgage_list(asset_index)

                            else:
                                self.logObj.printer("Your cash balance is negative ($%d) so can not exit. Please mortgage some assets or sell some buildings and get some cash to remain in game." % (self.get_player_by_its_ID(player_id).getPlayerCashBalance() - amount))
                        else:
                            self.logObj.printer("You do not have any assets remaining with you!")
                    else:
                        assetSelectMenu = self.display_player_asset_list_with_buildings_menu(player_id)
                        if assetSelectMenu is not None:
                            optionGot = assetSelectMenu.runMenu()
                            if optionGot[0] != assetSelectMenu.getoptioncount():
                                asset_index = optionGot[1]
                                sellprice = self.get_player_by_its_ID(player_id).get_building_selling_price_from_asset_index(asset_index)
                                if self.get_player_by_its_ID(player_id).remove_property_of_country(asset_index):
                                    self.payment_channel(player_id, 5, sellprice, "building selling money transferred")
                                else:
                                    self.logObj.printer("You are not allowed to sell building of this country. Please try other country.")
                            else:
                                self.logObj.printer("Your cash balance is negative ($%d) so can not exit. Please mortgage some assets or sell some buildings and get some cash to remain in game." % (self.get_player_by_its_ID(player_id).getPlayerCashBalance() - amount))
                        else:
                            self.logObj.printer("You do not have any assets remaining with you!")
                return True
            else:
                self.logObj.printer("Player-%d is not able to pay the amount as bankrupt and deposited all the assets/cash to bank.\nBye!!!" % player_id)
                self.remove_player_from_game(player_id)
                if len(self.Players) == 1:
                    self.set_game_state(-1)
                return False
        else:
            return True

    def surrender_all_assets_to_bank(self, player_id):
        for i in range(len(self.country_objs)):
            if self.country_objs[i].get_ownership() == player_id:
                self.properties_board_locations[self.country_objs[i].get_board_location()] = ""
                self.country_objs[i].set_ownership(0)
            if self.country_objs[i].get_ownership() == (player_id + 10):
                self.properties_board_locations[self.country_objs[i].get_board_location()] = ""
        for i in range(len(self.utility_objs)):
            if self.utility_objs[i].get_ownership() == player_id:
                self.properties_board_locations[self.utility_objs[i].get_board_location()] = ""
                self.utility_objs[i].set_ownership(0)
            if self.utility_objs[i].get_ownership() == (player_id + 10):
                self.properties_board_locations[self.utility_objs[i].get_board_location()] = ""
        for i in self.get_player_by_its_ID(player_id).getPlayerAssetList():
            i.set_ownership(0)
            self.Banker.asset_list.append(i)
            if i.isSite():
                self.Banker.asset_group_counter[i.get_group()] += 1
        tmp_asset_list = []
        for i in range(len(self.Banker.mortgage_ownership)):
            if self.Banker.mortgage_ownership[i].get_ownership() == (player_id + 10):
                tmp_asset_list.append(self.Banker.mortgage_ownership[i])
                self.Banker.mortgage_ownership[i].set_ownership(0)
                self.Banker.asset_list.append(self.Banker.mortgage_ownership[i])
                if self.Banker.mortgage_ownership[i].isSite():
                    self.Banker.asset_group_counter[self.Banker.mortgage_ownership[i].get_group()] += 1
        for i in tmp_asset_list:
            self.Banker.mortgage_ownership.remove(i)

    def print_movement_info(self, player_id):
        location_name = self.get_position_name_where_player_standing(player_id)
        location_rent = self.get_property_rent_where_player_standing(player_id)
        if location_rent != -1:
            self.logObj.printer("You reached on %s which attracts rent of $%d." % (location_name, location_rent))
        else:
            self.logObj.printer("You reached on %s." % location_name)

    def player_payment_on_crossover(self, player_id):
        self.receive_reward(player_id, 1500, "Crossover Payment")

    def get_winner(self):
        winner = self.Players[0]
        for i in self.Players:
            if i.player_assets_valuation() > winner.player_assets_valuation():
                winner = i
        return winner.getPlayerID()

    def payment_channel(self, recipient, sender, amount, transaction_description):
        if 1 <= sender <= 4:
            sender_name = "Player-%d" % sender
        else:
            sender_name = "Bank"
        if 1 <= recipient <= 4:
            receiver_name = "Player-%d" % recipient
        else:
            receiver_name = "Bank"
        if 1 <= sender <= 4:
            res = self.check_a_player_if_negative_bal_after_deduction(sender, amount)
        else:
            res = self.check_bank_with_negative_cash(amount)
        if res is True:
            self.get_player_by_its_ID(sender).get_from_me(amount, "%s: %s" % (receiver_name,
                                                                                         transaction_description))
            self.get_player_by_its_ID(recipient).pay_to_me(amount, "%s: %s" % (sender_name,
                                                                                             transaction_description))
        else:
            self.logObj.printer("Transaction failed as %s is not able to pay the amount as become bankrupt." % sender_name)

    def display_player_sites_list_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerMortgagedAssetList()) == 0:
            if len(self.get_player_by_its_ID(player_id).getSitesIndices()) > 0:
                assetsMenu = MenuBox("Player Sites List", self.logPath)
                for i in self.get_player_by_its_ID(player_id).getSitesIndices():
                    assetsMenu.addOption(self.get_player_by_its_ID(player_id).get_assetObj_from_index(i).get_name_with_building_price())
                return assetsMenu
            else:
                self.logObj.printer("No asset available for Player-%d" % player_id)
                return None
        else:
            self.logObj.printer("There are already mortgaged properties (%s). First redeem them." % self.get_player_by_its_ID(player_id).getPlayerMortgagedRealEstateShort())

    def build_property_on_player_site(self, player_id):
        self.logObj.printer("Player cash balance = %d" % self.get_player_by_its_ID(player_id).getPlayerCashBalance())
        assetSelectMenu = self.display_player_sites_list_menu(player_id)
        site_indices_list = self.get_player_by_its_ID(player_id).getSitesIndices()
        if assetSelectMenu is not None:
            optionGot = assetSelectMenu.runMenu()
            if optionGot != assetSelectMenu.getoptioncount():
                asset_index = site_indices_list[optionGot - 1]
                asset_name = self.get_player_by_its_ID(player_id).get_assetObj_from_index(asset_index).get_name()
                building_price = self.get_player_by_its_ID(player_id).get_assetObj_from_index(asset_index).get_building_price()
                if self.get_player_by_its_ID(player_id).getPlayerCashBalance() > building_price:
                    if self.get_player_by_its_ID(player_id).add_property_on_country(asset_index):
                        self.payment_channel(5, player_id, building_price, "building on %s money transfer" % asset_name)
                        self.logObj.printer("Now cash balance = $%d" % self.get_player_by_its_ID(player_id).getPlayerCashBalance())
                else:
                    self.logObj.printer("Not enough cash balance to raise more buildings.")
            else:
                self.logObj.printer("Not interested in buying")
        else:
            self.logObj.printer("You do not have any eligible site remaining with you to build property upon!")
