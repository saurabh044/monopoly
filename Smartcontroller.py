from MenuBox import MenuBox
from MenuBox2 import MenuBox2
from Banksmart import Banksmart, Transaction
from Smartplayer import Smartplayer
from Asset import Country 
from Asset import Utility
import re
from Printer import Printer
import random


# Game Board Data
# key value array of country [boardPosition, buyValue, mortgageValue, colorGroup, basicRent, property_price, property_rent]
country_list = {"England":   [ 2, 7000, 3500, 1, 700, 7000, 1700],
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
# key value array of Utility [boardPosition, buyValue, mortgageValue, rent, pair_rent, group_id]
utility_list = {"Waterways": [4, 9500, 2000, 1400, 2200, 1],
                "Satellite": [8, 2000, 1250, 500, 1000, 1],
                "Airways": [13, 10500, 5500, 1500, 2500, 3],
                "Roadways": [23, 3500, 1800, 800, 1500, 2],
                "Petroleum": [32, 5500, 1300, 500, 1000, 3],
                "Railways": [34, 9500, 5000, 1500, 2500, 2]
                }
board_display_data = ["Start", "England R-2500", "Iraq G-5000", 
                      "Waterways U-9500", "UNO",
                      "France R-2500", "Iran G-2500", "Satellite U-2000",
                      "Egypt G-3200", "Resort", "Canada Y-4000", 
                      "Germany R-3500", "Airways U-10500", "Custom-Duty",
                      "Swiss R-3500", "Brazil Y-2500", "Chance",
                      "Italy R-3500", "Party-House", "Japan B-2500",
                      "USA Y-8500", "Travelling-Duty", "Roadways U-3500",
                      "Mexico Y-4000", "Hongkong B-2000", "UNO", 
                      "Australia Y-3300", "Jail", "India B-5500", "Chance", 
                      "SaudiArab G-5500", "Petroleum U-5500", "China B-4500", 
                      "Railways U-9500", "Malaysia G-1500", 
                      "Singapore B-3000"]
assets_board_locations = { 2: "",  3: "",  4: "",  6: "",
                           7: "",  8: "",  9: "", 11: "",
                          12: "", 13: "", 15: "", 16: "",
                          18: "", 20: "", 21: "", 23: "",
                          24: "", 25: "", 27: "", 29: "",
                          31: "", 32: "", 33: "", 34: "",
                          35: "", 36: ""}
        
class Dice(object):

    def __init__(self):
        self.val = 0

    def throw_dice(self):
        out = random.randint(2, 12)
        return out
    
    
class Smartcontroller(object):

    crossover_amount = 100
    def __init__(self, player_count, log_path):
        self.logPath = log_path
        self.gamePlayMenu = MenuBox("Play Game", self.logPath)
        self.gamePlayMenu.addOption("Roll Dice")

        self.PlayerMenu = MenuBox("Player Menu", self.logPath)
        self.PlayerMenu.addOption("Continue")
        self.PlayerMenu.addOption("Redeem")
        self.PlayerMenu.addOption("Build Property")
        self.PlayerMenu.addOption("Sell Property")
        self.PlayerMenu.addOption("Buy Other Player Country")
        self.PlayerMenu.addOption("Mortgage")

        self.PlayerBuyMenu = MenuBox("Buy Menu", self.logPath)
        self.PlayerBuyMenu.addOption("Want to buy")
        
        self.logObj = Printer(self.logPath)
        self.player_count = player_count
        self.players = []
        self.dice = Dice()
        self.available_players_index = {}
        for i in range(self.player_count):
            # inp = raw_input("Enter name for Player-%d : " % (i+1)) # simulation
            inp = 'PL-' + str(i+1) # simulation
            self.players.append(Smartplayer(i+1, str(inp), self.logPath)) 
            self.available_players_index[i+1] = i
            self.players[i].set_statement_filename("./business_game_logs/Player-%d_account_statement.txt" % (i+1))
        self.turnHolderPlayerID = 0
        self.BoardData = {}
        self.state = True
        for i in range(36):
            self.BoardData[i+1] = []
        self.country_name_list = ["England", "Iraq", "France", "Iran", "Egypt", "Canada", "Germany", "Swiss", "Brazil",
                                  "Italy", "Japan", "USA", "Mexico", "Hongkong", "Australia", "India", "SaudiArab",
                                  "China", "Malaysia", "Singapore"]
        # key value array of Utility [boardPosition, buyValue, mortgageValue]
        self.utility_name_list = ["Waterways", "Satellite", "Airways", "Roadways", "Petroleum", "Railways"]
        self.Banker = Banksmart(0, self.logPath)
        # Initialize the bank cash reserve with $1000000
        self.Banker.process_request(Transaction(-1, 0, 12, 1000000, "Cash reserved to bank"))
        self.Banker.add_players_accounts(self.player_count)
        # Initial payment of $25000 to all the players for starting the game 
        for i in range(self.player_count):
            self.Banker.process_request(Transaction(0, i+1, 11, 25000, "Initial Payment"))

        for i in country_list:
            self.Banker.asset_list.append(Country(country_list[i][0], i,
                                             country_list[i][1],
                                             country_list[i][2],
                                             country_list[i][4],
                                             country_list[i][5],
                                             country_list[i][6],
                                             country_list[i][3]))
        for i in utility_list:
            self.Banker.asset_list.append(Utility(utility_list[i][0], i, 
                                             utility_list[i][1], 
                                             utility_list[i][2], 
                                             utility_list[i][3], 
                                             utility_list[i][4],
                                             utility_list[i][5]))

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
            
    def set_turn(self, value):
        x = False
        while x == False:
            check_key = (value + self.turnHolderPlayerID) % (self.player_count + 1)
            if check_key in self.available_players_index.keys():
                x = True
                self.turnHolderPlayerID = check_key
            else:
                if value > 0: 
                    value += 1
                else:
                    value -= 1 

    def remove_player_from_game(self, player_id):
        self.Banker.bankrupt_a_player(player_id)
        self.players[player_id-1].deactivate()
        if len(self.players) > 2:
            if self.turnHolderPlayerID == player_id:
                self.set_turn(-1)
            del self.available_players_index[player_id]
            

    def next_move(self, chance):
        self.logObj.printer("Chance #%d" % chance)
        if self.state:
            self.set_turn(1)
        turnplayer = self.get_player_by_its_ID(self.turnHolderPlayerID)
        self.logObj.printer("Player %s, your chance" % turnplayer.name) 
        optionGameRecv = self.gamePlayMenu.auto_runMenu(1) # simulation line
        if optionGameRecv == 1:
            dice_out = self.dice.throw_dice()
            self.logObj.printer("Dice outcome = %d" % dice_out)
            iscrossover = turnplayer.move(dice_out)
            target_loc = turnplayer.board_pos
            if iscrossover:
                self.Banker.process_request(Transaction(0, turnplayer.id, 13, Smartcontroller.crossover_amount, 'Crossover payment'))
            ownerID = self.get_property_owner_where_player_standing(turnplayer)
            if ownerID == -1:
                player_pos = self.get_board_position_where_player_standing(turnplayer)
                if player_pos == 5 or player_pos == 26:  # UNO
                    self.apply_uno_to_player(turnplayer.id, dice_out)
                elif player_pos == 17 or player_pos == 30:  # CHANCE
                    self.apply_chance_to_player(turnplayer.id, dice_out)
                elif player_pos == 14:  # custom duty
                    self.payCustomDuty(turnplayer.id)
                elif player_pos == 22:  # travelling duty
                    self.payTravellingDuty(turnplayer.id)
                elif player_pos == 28:  # JAIL
                    self.gotojail(turnplayer.id)
                elif player_pos == 10:  # Resort
                    self.enjoyment_in_resort(turnplayer.id)
                elif player_pos == 19:  # Party House
                    self.get_party_from_others(turnplayer.id)
                else:
                    pass
            else:
                result = self.Banker.sell_asset_to_player(turnplayer.id, turnplayer.board_pos)
                if result == 0:
                    assets_board_locations[turnplayer.board_pos] = "|P%d|" % turnplayer.id
                elif result == -1:
                    self.remove_player_from_game(turnplayer.id)
                else:
                    pass
            self.display_board()
            self.print_all_player_assets_table()
            if self.state:
                optionPlayerRecv = 0
                while optionPlayerRecv != 1:
                    if chance < 500:
                        optionPlayerRecv = self.PlayerMenu.auto_runMenu(1)
                    else:
                        optionPlayerRecv = self.PlayerMenu.runMenu()
                    if optionPlayerRecv == 1:
                        self.logObj.printer("Continuing the game...\n")
                    elif optionPlayerRecv == 2:
                        self.logObj.printer("Player %d wants to redeem his mortgaged assets" % self.turnHolderPlayerID)
                        self.redeem_mortgaged_property_of_player(self.turnHolderPlayerID)
                    elif optionPlayerRecv == 3:
                        self.logObj.printer("Player %d wants to build property on his site" % self.turnHolderPlayerID)
                        self.build_property_on_player_site(self.turnHolderPlayerID)
                    else:
                        pass

    def get_player_by_its_ID(self, ids):
        if ids == 0:
            return self.Banker
        else:
            return self.players[self.available_players_index[ids]]

    def get_player_cash_balance(self, ids):
        return self.Banker.accounts[ids].balance

    def print_all_player_assets_table(self):
        total_cash_reserver = 0
        total_asset_reserver = 0
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format("PID", "Name", "Cash", "NetWorth", "Assets"))
        for i in self.players:
            if i.active:
                total_cash_reserver += self.Banker.get_players_balance(i.id)
                total_asset_reserver += self.Banker.get_players_asset_value(i.id)
                self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format(i.id,
                                                                                   i.name, 
                                                                                   self.Banker.get_players_balance(i.id), 
                                                                                   self.Banker.get_players_asset_value(i.id),
                                                                                   self.Banker.group_wise_asset_list(i.id)))
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format("BID", "Name", "Cash", "NetWorth", "Assets"))
        self.logObj.printer("{: <5} {: <10} {: >8} {: >10} {: <10}".format(0,
                                                                           'Bank',
                                                                           self.Banker.get_players_balance(0),
                                                                           self.Banker.get_players_asset_value(0),
                                                                           self.Banker.group_wise_asset_list(0)))
        total_cash_reserver += self.Banker.get_players_balance(0)
        total_asset_reserver += self.Banker.get_players_asset_value(0)
        if total_cash_reserver != 1000000:
            self.logObj.printer("Cash-Balance issue occurred.")
            raise ValueError
        if total_asset_reserver != 118000:
            self.logObj.printer("Asset-Balance issue occurred.")
            raise ValueError
        self.logObj.printer("")

    def display_board(self):
        i = 0
        while i < len(board_display_data):
            pp = self.check_all_player_presence_on_a_position(i+1)
            if (i+1) in assets_board_locations:
                owner_tag = assets_board_locations[i+1]
            else:
                owner_tag = ""
            loc = ""
            for j in range(len(pp)):
                if pp[j]:
                    loc = loc + "<P" + str(pp[j].id) + ">"
            self.BoardData[i+1] = [board_display_data[i], owner_tag, loc]
            i += 1
        self.logObj.printer("--------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(9):
            self.logObj.printer("{: >16} {: <6} {: <16} {: >16} {: <6} {: <16} {: >16} {: <6} {: <16} {: >16} {: <6} {: <16}".format(
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
        self.logObj.printer("--------------------------------------------------------------------------------------------------------------------------------------------------------\n")


    def get_property_owner_where_player_standing(self, playerobj):
        if playerobj.board_pos in assets_board_locations:
            return self.Banker.get_owner_by_assetid(playerobj.board_pos)
        else:
            return -1

    def get_property_rent_where_player_standing(self, player):
        board_pos = player.board_pos
        return self.Banker.get_current_rent_by_assetid(board_pos)

    def get_position_name_where_player_standing(self, player):
        return board_display_data[player.board_pos-1].split(' ')[0]

    def get_board_position_where_player_standing(self, player):
        return player.board_pos

    def transmit_from_one_to_rest(self, sender, amount, reason_text):
        for i in self.players:
            if i.active:
                if i.id != sender:
                    self.Banker.process_request(Transaction(sender, i.id, 11, amount, reason_text))

    def receive_from_all_to_one(self, receiver, amount, reason_text):
        for i in self.players:
            if i.active:
                if i.id != receiver:
                    self.Banker.process_request(Transaction(i.id, receiver, 11, amount, reason_text))

    def pay_fine(self, culprit, amount, reason_text):
        self.Banker.process_request(Transaction(culprit, 0, 14, amount, reason_text))

    def receive_reward(self, recipient, amount, reason_text):
        self.Banker.process_request(Transaction(0, recipient, 11, amount, reason_text))      

    def payCustomDuty(self, recipient): 
        self.Banker.process_request(Transaction(recipient, 0, 15, None, "Custom Duty"))

    def payTravellingDuty(self, recipient):
        self.Banker.process_request(Transaction(recipient, 0, 16, None, "Travelling Duty"))

    def enjoyment_in_resort(self, player_id):
        self.transmit_from_one_to_rest(player_id, 200, "Resort money")

    def get_party_from_others(self, player_id):
        self.receive_from_all_to_one(player_id, 200, "Reached party house")

    def gotojail(self,player_id):
        self.pay_fine(player_id, 100, "Reached on Jail")
        
    def check_all_player_presence_on_a_position(self, board_pos):
        pres = []
        for i in self.players:
            if i.active:
                if i.board_pos == board_pos:
                    pres.append(i)
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
            for i in self.players:
                if i.id == recipient:
                    i.jump(19)
        elif rule_num == 10:
            self.logObj.printer("Receive interest on shares of $1500.")
            self.receive_reward(recipient, 1500, "UNO-10: shares interest")
        elif rule_num == 12:
            self.logObj.printer("Receive amount of $3000 after sale of stocks.")
            self.receive_reward(recipient, 3000, "UNO-12: sale of stocks")
        elif rule_num == 3:
            self.logObj.printer("Go to jail.")
            self.pay_fine(recipient, 500, "UNO-3: Sent to Jail.")
            for i in self.players:
                if i.id == recipient:
                    i.jump(28)
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
            for i in self.players:
                if i.id == recipient:
                    i.jump(28)
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
            self.Banker.process_request(Transaction(None, recipient, 5, 7, "Chance-7: Rent collection"))
        elif rule_num == 9:
            self.logObj.printer("You have won the jackpot of $2000.")
            self.receive_reward(recipient, 2000, "Chance-9: won jackpot")
        elif rule_num == 11:
            self.logObj.printer("Prize for best performance in export of $1500.")
            self.receive_reward(recipient, 1500, "Chance-11: Best exporter")
        else:
            pass

    def display_player_mortgaged_asset_list_menu(self, player_id):
        if len(self.get_player_by_its_ID(player_id).getPlayerMortgagedAssetList()) > 0:
            assetsMenu = MenuBox("Mortgaged Asset List", self.logPath)
            for i in self.get_player_by_its_ID(player_id).getPlayerMortgagedAssetList():
                assetsMenu.addOption(i.get_name_with_mortgage_value())
            return assetsMenu
        else:
            self.logObj.printer("No asset is mortgaged to bank for Player-%d" % player_id)
            return None

    def set_game_state(self, state):
        self.gameState = state  # only 0, 1, -1 allowed in input. 0: inactive, 1: active, -1: finished , -2: Draw

    def get_winner_name(self):
        return self.Players[0].getPlayerName()

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

    def get_winner(self):
        winner = self.Players[0]
        for i in self.Players:
            if i.active:
                if i.player_assets_valuation() > winner.player_assets_valuation():
                    winner = i
        return winner.getPlayerID()

    def build_property_on_player_site(self, player_id):
        player_props = []
        for i in self.Banker.asset_list:
            if i.issite():
                if i.owner == player_id and i.prop_vacancy:
                    player_props.append(i)
        if len(player_props) > 0:  
            prop_buy_menu = MenuBox('Building Purchase Menu', self.logPath)
            for i in player_props:
                prop_buy_menu.addOption(i.name)
            optionGot = prop_buy_menu.runMenu()
            if optionGot != prop_buy_menu.getoptioncount():
                asset_id = player_props[optionGot - 1].board_loc
                self.Banker.sell_building_to_player(player_id, asset_id)
            else:
                self.logObj.printer("Not interested in buying")
        else:
            self.logObj.printer("You do not have any eligible site to build property upon!")
  