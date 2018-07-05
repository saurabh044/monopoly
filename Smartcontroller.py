from MenuBox import MenuBox, Printer, Dice, DBhandler, color_coded
from Banksmart import Banksmart
from Asset import Country, Utility
from colorama import init, Fore, Back, Style
import re
import os
import platform


# Game Board Data
# key value array of country [boardPosition, buyValue, mortgageValue, colorGroup, basicRent, property_price, property_rent]
country_list = {"England":   ( 2, 7000, 3500, 1, 700, 7000, 1700),
                "Iraq":      ( 3, 5000, 2500, 2, 500, 5000, 1500),
                "France":    ( 6, 2500, 1250, 1, 300, 2500, 1300),
                "Iran":      ( 7, 2500, 1250, 2, 300, 2500, 1300),
                "Egypt":     ( 9, 3200, 1500, 2, 300, 3200, 1300),
                "Canada":    (11, 4000, 2000, 4, 400, 4000, 1400),
                "Germany":   (12, 3500, 1750, 1, 400, 3500, 1400),
                "Swiss":     (15, 3500, 3300, 1, 700, 6500, 1700),
                "Brazil":    (16, 2500, 1300, 4, 300, 2500, 1300),
                "Italy":     (18, 3500, 1000, 1, 200, 2000, 1200),
                "Japan":     (20, 2500, 1250, 3, 250, 2500, 1250),
                "USA":       (21, 8500, 5000, 4, 1000, 8500, 2000),
                "Mexico":    (24, 4000, 2000, 4, 900, 4000, 1800),
                "Hongkong":  (25, 2000, 1000, 3, 200, 2500, 1200),
                "Australia": (27, 3300, 2000, 4, 400, 3300, 1400),
                "India":     (29, 5500, 2750, 3, 550, 5500, 1550),
                "SaudiArab": (31, 5500, 2800, 2, 600, 5500, 1600),
                "China":     (33, 4500, 2250, 3, 450, 4500, 1450),
                "Malaysia":  (35, 1500,  800, 2, 200, 1500, 1200),
                "Singapore": (36, 3000, 1500, 3, 300, 3000, 1300)
                }
# key value array of Utility [boardPosition, buyValue, mortgageValue, rent, pair_rent, group_id]
utility_list = {"Waterways": (4, 9500, 2000, 1400, 2200, 1),
                "Satellite": (8, 2000, 1250, 500, 1000, 1),
                "Airways": (13, 10500, 5500, 1500, 2500, 3),
                "Roadways": (23, 3500, 1800, 800, 1500, 2),
                "Petroleum": (32, 5500, 1300, 500, 1000, 3),
                "Railways": (34, 9500, 5000, 1500, 2500, 2)
                }
board_display_data = ((color_coded[6] + color_coded[9] + "1-Start           " + color_coded[8] + color_coded[7]), 
                      (color_coded[1] + color_coded[9] + "2-England    $2500" + color_coded[8] + color_coded[7]), 
                      (color_coded[2] + color_coded[9] + "3-Iraq       $5000" + color_coded[8] + color_coded[7]), 
                      (color_coded[5] + color_coded[9] + "4-Waterways  $9500" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "5-UNO             " + color_coded[8] + color_coded[7]),
                      (color_coded[1] + color_coded[9] + "6-France     $2500" + color_coded[8] + color_coded[7]), 
                      (color_coded[2] + color_coded[9] + "7-Iran       $2500" + color_coded[8] + color_coded[7]), 
                      (color_coded[5] + color_coded[9] + "8-Satellite  $2000" + color_coded[8] + color_coded[7]),
                      (color_coded[2] + color_coded[9] + "9-Egypt      $3200" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "10-Resort         " + color_coded[8] + color_coded[7]), 
                      (color_coded[4] + color_coded[9] + "11-Canada    $4000" + color_coded[8] + color_coded[7]), 
                      (color_coded[1] + color_coded[9] + "12-Germany   $3500" + color_coded[8] + color_coded[7]), 
                      (color_coded[5] + color_coded[9] + "13-Airways  $10500" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "14-Custom Duty    " + color_coded[8] + color_coded[7]),
                      (color_coded[1] + color_coded[9] + "15-Swiss     $3500" + color_coded[8] + color_coded[7]), 
                      (color_coded[4] + color_coded[9] + "16-Brazil    $2500" + color_coded[8] + color_coded[7]),
                      (color_coded[6] + color_coded[9] + "17-Chance         " + color_coded[8] + color_coded[7]),
                      (color_coded[1] + color_coded[9] + "18-Italy     $3500" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "19-Party House    " + color_coded[8] + color_coded[7]), 
                      (color_coded[3] + color_coded[9] + "20-Japan     $2500" + color_coded[8] + color_coded[7]),
                      (color_coded[4] + color_coded[9] + "21-USA       $8500" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "22-Travel Duty    " + color_coded[8] + color_coded[7]), 
                      (color_coded[5] + color_coded[9] + "23-Roadways  $3500" + color_coded[8] + color_coded[7]),
                      (color_coded[4] + color_coded[9] + "24-Mexico    $4000" + color_coded[8] + color_coded[7]), 
                      (color_coded[3] + color_coded[9] + "25-Hongkong  $2000" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "26-UNO            " + color_coded[8] + color_coded[7]), 
                      (color_coded[4] + color_coded[9] + "27-Australia $3300" + color_coded[8] + color_coded[7]),
                      (color_coded[6] + color_coded[9] + "28-Jail           " + color_coded[8] + color_coded[7]), 
                      (color_coded[3] + color_coded[9] + "29-India     $5500" + color_coded[8] + color_coded[7]), 
                      (color_coded[6] + color_coded[9] + "30-Chance         " + color_coded[8] + color_coded[7]), 
                      (color_coded[2] + color_coded[9] + "31-SaudiArab $5500" + color_coded[8] + color_coded[7]),
                      (color_coded[5] + color_coded[9] + "32-Petroleum $5500" + color_coded[8] + color_coded[7]),
                      (color_coded[3] + color_coded[9] + "33-China     $4500" + color_coded[8] + color_coded[7]), 
                      (color_coded[5] + color_coded[9] + "34-Railways  $9500" + color_coded[8] + color_coded[7]), 
                      (color_coded[2] + color_coded[9] + "35-Malaysia  $1500" + color_coded[8] + color_coded[7]), 
                      (color_coded[3] + color_coded[9] + "36-Singapore $3000" + color_coded[8] + color_coded[7]))
                      
assets_board_locations = { 2: "    ",  3: "    ",  4: "    ",  6: "    ",
                           7: "    ",  8: "    ",  9: "    ", 11: "    ",
                          12: "    ", 13: "    ", 15: "    ", 16: "    ",
                          18: "    ", 20: "    ", 21: "    ", 23: "    ",
                          24: "    ", 25: "    ", 27: "    ", 29: "    ",
                          31: "    ", 32: "    ", 33: "    ", 34: "    ",
                          35: "    ", 36: "    "}

class Smartplayer(object):
    

    def __init__(self, id, name, logPath, active=True):
        self.id = id
        self.name = name
        self.active = active
        self.board_pos = 1
          
    def move(self, value):
        self.board_pos += value
        if self.board_pos > 36:
            self.board_pos -= 36
            return True
        return False
        
    def state(self):
        return (self.id, self.name, self.active, self.board_pos) 
    
    def change_state(self, new_state):
        (self.active, self.board_pos) = new_state
            
class Smartcontroller(object):

    color_code = {1: Fore.LIGHTRED_EX, 2: Fore.LIGHTGREEN_EX, 3: Fore.LIGHTBLUE_EX, 4: Fore.LIGHTYELLOW_EX}
    crossover_amount = 100
    
    def __init__(self, player_count, log_path, user=None, password=None):       
        self.logPath = log_path
        self.dbuser = user
        self.dbpassword = password
        self.PlayerMenu = MenuBox("Game Menu", self.logPath, 0)
        self.PlayerMenu.addOptions(["Continue", "Redeem", "Build Property", "Sell Property", "Show Asset Info", "Quit Game"])
        if self.dbuser is not None:
            self.PlayerMenu.addOption('Save Game')
        self.PlayerBuyMenu = MenuBox("Buy Menu", self.logPath)
        self.PlayerBuyMenu.addOption("Want to buy")
        
        self.logObj = Printer(self.logPath)
        self.player_count = player_count
        self.players = []
        self.dice = Dice()
        self.available_players_id = []
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
        self.Banker.asset_list = [Country(country_list[i][0], i, country_list[i][1], country_list[i][2], country_list[i][4],
                                          country_list[i][5], country_list[i][6], country_list[i][3]) for i in country_list] + \
                                 [Utility(utility_list[i][0], i, utility_list[i][1], utility_list[i][2],  utility_list[i][3], 
                                             utility_list[i][4], utility_list[i][5]) for i in utility_list]
                        
    def set_turn(self, value):
        if self.turnHolderPlayerID == 0:
            self.turnHolderPlayerID += 1
        else:
            next_players_index = (self.available_players_id.index(self.turnHolderPlayerID) + value) % len(self.available_players_id)
            self.turnHolderPlayerID = self.available_players_id[next_players_index]

    def print_winner(self, name):
        self.logObj.printer(color_coded[11] + ("*" * 30 + "\n") * 2 + "The winner is %s\n" % name + ("*" * 30 + "\n") * 2 + color_coded[8])            

    def remove_player_from_game(self, player_id):
        if player_id == 0:
            self.logObj.printer(color_coded[10] +"Bank is out of cash." + color_coded[8])
            self.state = False         
            self.print_winner(self.get_winner())
        else:
            res = self.Banker.bankrupt_a_player(player_id)
            for i in res:
                assets_board_locations[i] = "    "
            self.players[player_id-1].active = False
            self.players[player_id-1].board_pos = 0
            if len(self.available_players_id) >= 2:
                if self.turnHolderPlayerID == player_id:
                    self.set_turn(-1)
                self.available_players_id.remove(player_id)
            if len(self.available_players_id) == 1:
                self.state = False
                self.print_winner(self.players[self.available_players_id[0]-1].name)
                
    def next_move(self, chance):
        self.logObj.printer(color_coded[11] + "Chance #%d" % chance + color_coded[8])
        if self.state:
            self.set_turn(1)
        turnplayer = self.players[self.turnHolderPlayerID-1]
        self.logObj.printer(color_coded[11] + "Player %s, your chance" % turnplayer.name + color_coded[8]) 
        optionGameRecv = 1
        if optionGameRecv == 1:
            dice_out = self.dice.throw_dice()
            self.logObj.printer("Dice outcome = %d" % dice_out)
            iscrossover = turnplayer.move(dice_out)
            self.show_board(color_coded[11] + "Chance #%d\nPlayer %s, your chance\nDice outcome = %d\n" % (chance, turnplayer.name, dice_out) + color_coded[8])
            if iscrossover:
                self.logObj.printer(color_coded[11]+ "You received crossover payment of $%d" % Smartcontroller.crossover_amount + color_coded[8])
                res = self.Banker.payreward(turnplayer.id, Smartcontroller.crossover_amount, 'Crossover payment to Player-%d' % turnplayer.id)
                self.bank_response_action(res)
            ownerID = self.get_property_owner_where_player_standing(turnplayer)
            if ownerID == -1:
                if turnplayer.board_pos == 5 or turnplayer.board_pos == 26:  # UNO
                    self.apply_uno_to_player(turnplayer.id, dice_out)
                elif turnplayer.board_pos == 17 or turnplayer.board_pos == 30:  # CHANCE
                    self.apply_chance_to_player(turnplayer.id, dice_out)
                elif turnplayer.board_pos == 14:  # custom duty
                    self.logObj.printer(color_coded[10] + 'You reached on Custom Duty' + color_coded[8])
                    res = self.Banker.p2ptransaction(turnplayer.id, 0, -1, "Custom Duty - Player-%d" % turnplayer.id)
                    self.bank_response_action(res)
                elif turnplayer.board_pos == 22:  # travelling duty
                    self.logObj.printer(color_coded[10] + 'You reached on Travelling Duty' + color_coded[8])
                    res = self.Banker.p2ptransaction(turnplayer.id, 0, -1, "Travelling Duty - Player-%d" % turnplayer.id)
                    self.bank_response_action(res)
                elif turnplayer.board_pos == 28:  # JAIL
                    self.gotojail(turnplayer.id)
                elif turnplayer.board_pos == 10:  # Resort
                    self.enjoyment_in_resort(turnplayer.id)
                elif turnplayer.board_pos == 19:  # Party House
                    self.get_party_from_others(turnplayer.id)
                else:
                    pass
            else:
                result = self.Banker.sell_asset_to_player(turnplayer.id, turnplayer.board_pos)
                if result == 0:
                    assets_board_locations[turnplayer.board_pos] = Smartcontroller.color_code[turnplayer.id] + "|P%d|" % turnplayer.id + color_coded[8]
                elif result == -1:
                    self.remove_player_from_game(turnplayer.id)
                else:
                    self.Banker.auction_of_asset(turnplayer.board_pos)
            if self.state:
                optionPlayerRecv = 0
                while optionPlayerRecv not in (1, 6, 7) :
                    self.logObj.printer(color_coded[9+self.turnHolderPlayerID] + "Player-%d (%s)...\n" % (self.turnHolderPlayerID, turnplayer.name) + color_coded[8])
                    optionPlayerRecv = self.PlayerMenu.runMenu()
                    if optionPlayerRecv == 1:
                        self.logObj.printer("Continuing the game...\n")
                        self.show_board()
                    elif optionPlayerRecv == 2:
                        self.logObj.printer("Player %d wants to redeem his mortgaged assets" % self.turnHolderPlayerID)
                        self.redeem_mortgaged_property_of_player(self.turnHolderPlayerID)
                    elif optionPlayerRecv == 3:
                        self.logObj.printer("Player %d wants to build property on his site" % self.turnHolderPlayerID)
                        self.build_property_on_player_site(self.turnHolderPlayerID)
                    elif optionPlayerRecv == 4:
                        self.logObj.printer("Player %d wants to sell property of his site" % self.turnHolderPlayerID)
                        self.sell_property_of_player_site(self.turnHolderPlayerID)
                    elif optionPlayerRecv == 5:
                        select = 0
                        while select == False:
                            inp = raw_input("Enter the asset code: ")
                            self.logObj.printer("")
                            matchObj = re.match(r'^(\d+)$', inp, re.M)
                            if matchObj:
                                if 1 <= int(matchObj.group(1)) <= 36:
                                    select = int(inp)
                                else:
                                    self.logObj.printer(color_coded[10] + "Please enter valid asset code between 2 and 36." + color_coded[8])
                            else:
                                self.logObj.printer(color_coded[10] + "Please enter valid asset code between 2 and 36." + color_coded[8])
                        asset = self.Banker.get_asset_by_assetid(select)
                        if asset is not None:
                            self.logObj.printer(asset.info())
                        else:
                            self.logObj.printer(color_coded[10] + 'Input asset code is not valid. Please check the board.' + color_coded[8])
                    elif optionPlayerRecv == 6:
                        self.logObj.printer(color_coded[10] + 'Player-%d (%s) is leaving the game.' % (self.turnHolderPlayerID, turnplayer.name) + color_coded[8])
                        self.logObj.printer(color_coded[11] + 'Only %d players left in the game' % (len(self.available_players_id)-1)+ color_coded[8])
                        self.remove_player_from_game(self.turnHolderPlayerID)
                    elif optionPlayerRecv == 7:
                        if len(self.available_players_id) > 1: 
                            self.save_game(chance)
                        else:
                            self.logObj.printer("Game already finished. It can not be saved.")
                        self.state = False
                    else:
                        pass

    def print_all_player_assets_table(self, term_only):
        output = ""
        total_cash_reserver = self.Banker.get_players_balance(0) + reduce(lambda x, y: x + y, [self.Banker.get_players_balance(i.id) for i in self.players if i.active])
        total_asset_reserver = self.Banker.get_players_asset_value(0) + reduce(lambda x, y: x + y, [self.Banker.get_players_asset_value(i.id) for i in self.players if i.active])
        output += '-' * 118 + '\n'
        output += "|PID   |Name      |    Cash| NetWorth |    Assets Counters    |Asset Names                                                \n" 
        output += '-' * 118 + '\n'
        for i in self.players:
            if i.active:
                output += "|{: <5} |{: <10}|{: >8}|{: >10}|{: <10}\n".format(i.id, i.name, 
                                    self.Banker.get_players_balance(i.id), self.Banker.get_players_asset_value(i.id),
                                    self.Banker.group_wise_asset_list(i.id))
                output += '-' * 118 + '\n'
        output += "|{: <5} |{: <10}|{: >8}|{: >10}|{: <10}\n".format(0, 'Bank',
                            self.Banker.get_players_balance(0), self.Banker.get_players_asset_value(0), self.Banker.group_wise_asset_list(0))
        output += '-' * 118 + '\n'
        if total_cash_reserver != 1000000:
            output += "Cash-Balance issue occurred.\n"
            raise ValueError
        if total_asset_reserver != 118000:
            output += "Asset-Balance issue occurred.\n"
            raise ValueError
        if term_only is False: self.logObj.printer(output)
        else: print output
                        
    def display_board(self, term_only):
        output = ' ' * 71 + '-' * 24 + '\n' + ' ' * 71 +  color_coded[1] + color_coded[9]  + '|INTERNATIONAL BUSINESS|' + color_coded[8] + color_coded[7] +'\n' + ' ' * 71 + '-' * 24 + '\n'      
        i = 0
        while i < len(board_display_data):
            pp = self.check_all_player_presence_on_a_position(i+1)
            if (i+1) in assets_board_locations:
                owner_tag = assets_board_locations[i+1]
            else:
                owner_tag = "    "
            loc = ""
            for j in range(len(pp)):
                if pp[j]:
                    loc = loc + Smartcontroller.color_code[pp[j].id] + "<P" + str(pp[j].id) + ">" + color_coded[8]
            loc = loc + "    " * (self.player_count - len(pp))
            self.BoardData[i+1] = [board_display_data[i], owner_tag, loc]
            i += 1
        pl_col_len = 133 + 16*(self.player_count-2)
        output += '-' * pl_col_len + '\n'
        output += "|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n" % (
                                'Location          ', 'Own ', 'Player  ' + ' '*4*(self.player_count-2), 
                                'Location          ', 'Own ', 'Player  ' + ' '*4*(self.player_count-2),
                                'Location          ', 'Own ', 'Player  ' + ' '*4*(self.player_count-2),
                                'Location          ', 'Own ', 'Player  ' + ' '*4*(self.player_count-2))
        output += '-' * pl_col_len + '\n'
        for i in range(9):
            output += "|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n" % (
                                self.BoardData[i + 1][0], self.BoardData[i + 1][1], self.BoardData[i + 1][2], 
                                self.BoardData[i + 10][0], self.BoardData[i + 10][1],self.BoardData[i + 10][2],
                                self.BoardData[i + 19][0], self.BoardData[i + 19][1],self.BoardData[i + 19][2],
                                self.BoardData[i + 28][0], self.BoardData[i + 28][1],self.BoardData[i + 28][2])
        output += '-' * pl_col_len + '\n'
        if term_only is False:
            self.logObj.printer(output)
        else:
            print output
            
    def get_property_owner_where_player_standing(self, playerobj):
        return self.Banker.get_owner_by_assetid(playerobj.board_pos)

    def show_board(self, msg="", term_only=False):
        if platform.system() == 'Linux':
            _ = os.system('clear')
        else:
            _ = os.system('cls')   
        self.display_board(term_only)
        self.print_all_player_assets_table(term_only)
        self.logObj.printer(msg) 
        
    def transmit_from_one_to_rest(self, sender, amount, reason_text):
        for i in self.available_players_id:
            if i != sender:
                res = self.Banker.p2ptransaction(sender, i, amount, reason_text)
                self.bank_response_action(res)
                if sender in res:
                    break

    def receive_from_all_to_one(self, receiver, amount, reason_text):
        for i in self.available_players_id:
            if i != receiver:
                res = self.Banker.p2ptransaction(i, receiver, amount, reason_text)
                self.bank_response_action(res)

    def enjoyment_in_resort(self, player_id):
        self.logObj.printer(color_coded[10] + 'You reached on Resort. Paid $200 to all.'+ color_coded[8])
        self.transmit_from_one_to_rest(player_id, 200, "Resort money - Player-%d" % player_id)

    def get_party_from_others(self, player_id):
        self.logObj.printer(color_coded[11] + 'You reached on Party House. Eligible to receive $200 from all.'+ color_coded[8])
        self.receive_from_all_to_one(player_id, 200, "Party House - Player-%d" % player_id)

    def gotojail(self,player_id):
        self.logObj.printer(color_coded[10] + 'You reached on Jail. Paid $ 100 to come out.'+ color_coded[8])
        res = self.Banker.p2ptransaction(player_id, 0, 100, "Reached to Jail - Player-%d" % player_id)
        self.bank_response_action(res)
        
    def check_all_player_presence_on_a_position(self, board_pos):
        return [i for i in self.players if i.active and i.board_pos == board_pos]

    def apply_uno_to_player(self, recipient, rule_num):
        if rule_num == 2:
            self.logObj.printer(color_coded[11] + "UNO-2: It is your anniversary, collect $500 from each player." + color_coded[8])
            self.receive_from_all_to_one(recipient, 500, "UNO-2: Anniversary gift - Player-%d" % recipient)
        elif rule_num == 4:
            self.logObj.printer(color_coded[11] + "UNO-4: 1st prize in Beauty Contest of $2500." + color_coded[8])
            res = self.Banker.payreward(recipient, 2500, "UNO-4, Won Beauty Contest - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 6:
            self.logObj.printer(color_coded[11] + "UNO-6: Income tax refund of $2000." + color_coded[8])
            res = self.Banker.payreward(recipient, 2000, "UNO-6, IT refund - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 8:
            self.logObj.printer(color_coded[11] + "UNO-8: Go to party house and collect $200 from each player." + color_coded[8])
            self.receive_from_all_to_one(recipient, 200, "UNO-8: Party house - Player-%d" % recipient)
            for i in self.players:
                if i.id == recipient:
                    i.board_pos = 19
        elif rule_num == 10:
            self.logObj.printer(color_coded[11] + "UNO-10: Receive interest on shares of $1500." + color_coded[8])
            res = self.Banker.payreward(recipient, 1500, "UNO-10: shares interest - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 12:
            self.logObj.printer(color_coded[11] + "UNO-12: Receive amount of $3000 after sale of stocks." + color_coded[8])
            res = self.Banker.payreward(recipient, 3000, "UNO-12: sale of stocks - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 3:
            self.logObj.printer(color_coded[10] + "UNO-3: Go to jail with $500 fine" + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 500, "UNO-3: Sent to Jail - Player-%d" % recipient)
            self.bank_response_action(res)
            for i in self.players:
                if i.id == recipient:
                    i.board_pos = 28
        elif rule_num == 5:
            self.logObj.printer(color_coded[10] + "UNO-5: School and medical fees expenses of $2500." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 2500, "UNO-5: School Fees - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 7:
            self.logObj.printer(color_coded[10] + "UNO-7: Submit your passport and pay $5000 fine." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 5000, "UNO-7: Passport Deposit - Player-%d" % recipient)
            self.bank_response_action(res)
        elif rule_num == 9:
            self.logObj.printer(color_coded[10] + "UNO-9: Make general repair on your properties of $100" + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0,  100, "UNO-9: Repair - Player-%d" % recipient)
            self.bank_response_action(res)            
        elif rule_num == 11:
            self.logObj.printer(color_coded[10] + "UNO-11: Pay insurance premium of $1500." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 1500, "UNO-11, Insurance Premium - Player-%d" % recipient)
            self.bank_response_action(res) 
        else:
            pass

    def apply_chance_to_player(self, recipient, rule_num):
        if rule_num == 2:
            self.logObj.printer(color_coded[10] + "Chance-2: Loss in share market of $2000." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 2000, "Chance-2: Loss in share - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 4:
            self.logObj.printer(color_coded[10] + "Chance-4: Fine for accident due to wrong driving of $1000" + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 1000, "Chance-4: Driving fine - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 6:
            self.logObj.printer(color_coded[10] + "Chance-6: House repair of $1500." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 1500, "Chance-6: House repair - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 8:
            self.logObj.printer(color_coded[10] + "Chance-8: Loss of $3000 due to fire in Go-down." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 3000, "Chance-8: Loss due to fire - Player-%d" % recipient)
            self.bank_response_action(res)             
        elif rule_num == 10:
            self.logObj.printer(color_coded[10] + "Chance-10: Go to jail." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 500, "Chance-10: Sent to jail - Player-%d" % recipient)
            self.bank_response_action(res)             
            for i in self.players:
                if i.id == recipient:
                    i.board_pos = 28
        elif rule_num == 12:
            self.logObj.printer(color_coded[10] + "Chance-12: Repair of your car of $200." + color_coded[8])
            res = self.Banker.p2ptransaction(recipient, 0, 200, "Chance-12: Car repair - Player-%d" % recipient)
            self.bank_response_action(res)             
        elif rule_num == 3:
            self.logObj.printer(color_coded[11] + "Chance-3: Won lottery prize of $2500." + color_coded[8])
            res = self.Banker.payreward(recipient, 2500, "Chance-3: won lottery - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 5:
            self.logObj.printer(color_coded[11] + "Chance-5: You have won cross-word prize of $1000." + color_coded[8])
            res = self.Banker.payreward(recipient, 1000, "Chance-5: won cross-word - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 7:
            self.logObj.printer(color_coded[11] + "Chance-7: Collect $100 rent from each player for all of your site." + color_coded[8])
            amount = self.Banker.get_players_countries(recipient) * 100
            self.receive_from_all_to_one(recipient, amount, "Chance-7: Rent collection - Player-%d" % recipient)
        elif rule_num == 9:
            self.logObj.printer(color_coded[11] + "Chance-9: You have won the jackpot of $2000." + color_coded[8])
            res = self.Banker.payreward(recipient, 2000, "Chance-9: won jackpot - Player-%d" % recipient)
            self.bank_response_action(res) 
        elif rule_num == 11:
            self.logObj.printer(color_coded[11] + "Chance-11: Prize for best performance in export of $1500." + color_coded[8])
            res = self.Banker.payreward(recipient, 1500, "Chance-11: Best exporter - Player-%d" % recipient)
            self.bank_response_action(res)             
        else:
            pass

    def redeem_mortgaged_property_of_player(self, player_id):
        player_mort_props = [i for i in self.Banker.asset_list if i.owner == player_id + 10]
        if len(player_mort_props) > 0:
            prop_redeem_menu = MenuBox('Asset Redemption Menu', self.logPath)  
            prop_redeem_menu.addOptions([i.name for i in player_mort_props])  
            optionGot = prop_redeem_menu.runMenu()
            if optionGot != prop_redeem_menu.getoptioncount():
                asset_id = player_mort_props[optionGot-1].board_loc
                self.Banker.redeem_asset_of_player(player_id, asset_id)
            else:
                self.logObj.printer("Not interested in redemption.")    
        else:
            self.logObj.printer(color_coded[11] + "You do not have any mortgaged assets." + color_coded[8])

    def build_property_on_player_site(self, player_id):
        player_props = [i for i in self.Banker.asset_list if i.issite() if i.owner == player_id and i.prop_vacancy]
        if len(player_props) > 0:  
            prop_buy_menu = MenuBox('Building Purchase Menu', self.logPath)
            prop_buy_menu.addOptions([i.name for i in player_props])
            optionGot = prop_buy_menu.runMenu()
            if optionGot != prop_buy_menu.getoptioncount():
                asset_id = player_props[optionGot-1].board_loc
                self.Banker.sell_building_to_player(player_id, asset_id)
            else:
                self.logObj.printer("Not interested in buying")
        else:
            self.logObj.printer("You do not have any eligible site to build property upon!")

    def sell_property_of_player_site(self, player_id):
        player_props = [i for i in self.Banker.asset_list if i.issite() if i.owner == player_id and i.prop_sell]
        if len(player_props) > 0:  
            prop_sell_menu = MenuBox('Building Sell Menu', self.logPath)
            prop_sell_menu.addOptions([i.name for i in player_props])
            optionGot = prop_sell_menu.runMenu()
            if optionGot != prop_sell_menu.getoptioncount():
                asset_id = player_props[optionGot-1].board_loc
                self.Banker.get_building_from_player(player_id, asset_id)
            else:
                self.logObj.printer("Not interested in selling")
        else:
            self.logObj.printer("You do not have any eligible site to sell property from!")
            
    def get_winner(self):
        winner = self.available_players_id[0]
        for i in self.available_players_id:
            if self.Banker.get_players_valuation(i) > self.Banker.get_players_valuation(winner):
                winner = i
        return self.players[winner-1].name
  
    def bank_response_action(self, player_list):
        for i in player_list:
            self.remove_player_from_game(i)
          
    def addplayersingame(self):
        for i in range(self.player_count):
            inp = raw_input(color_coded[11] + "Enter name for Player-%d : " % (i+1) + color_coded[8] ) 
            self.players.append(Smartplayer(i+1, str(inp)[0:10], self.logPath)) 
            self.available_players_id.append(i+1)
        # Initialize the bank cash reserve with $1000000
        self.Banker.add_players_accounts(self.player_count)
        self.Banker.accounts[0].deposit(1000000, "Cash reserved to bank")
        # Initial payment of $25000 to all the players for starting the game 
        for i in range(self.player_count):
            res = self.Banker.payreward(i+1, 25000, "Initial Payment - Player-%d" % (i+1)) 

    def save_game(self, chance_count):
        self.logObj.printer(color_coded[11] + "Saving game data into database..." + color_coded[8])
        try:
            dx = DBhandler(self.dbuser, self.dbpassword)
            if dx.isDBexist('monopoly_game_db') == 1:
                dx.dropDB('monopoly_game_db')
            dx.createDB("monopoly_game_db")
            dx.createTable('monopoly_game_db', 'player', ['id', 'name', 'active', 'board_pos', 'isavailable', 'isturnholder'],
                            ['tinyint primary key', 'varchar(30)', 'tinyint', 'tinyint', 'tinyint', 'int'])
            dx.createTable('monopoly_game_db', 'countries', ['board_loc', 'owner', 'current_rent', 'prop_count', 'prop_vacancy', 'prop_sell'],
                           ['tinyint primary key', 'tinyint', 'int', 'tinyint', 'tinyint', 'tinyint'])
            dx.createTable('monopoly_game_db', 'utilities', ['board_loc', 'owner', 'current_rent'],
                           ['tinyint primary key', 'tinyint', 'int'])
            dx.createTable('monopoly_game_db', 'accounts', ['id', 'balance', 'state'],
                           ['tinyint primary key', 'int', 'tinyint'])
            for i in self.players:
                isavail, isturn = 0, 0
                if i.id in self.available_players_id: isavail = 1
                if i.id == self.turnHolderPlayerID: isturn = chance_count
                dx.insertintoDB('monopoly_game_db', "INSERT INTO player values (%d, \'%s\', %d, %d, %d, %d)" % (i.state() + (isavail, isturn)))
    
            for i in self.Banker.asset_list:
                if i.issite():
                    dx.insertintoDB('monopoly_game_db', "INSERT INTO countries values (%d, %d, %d, %d, %d, %d)" % i.state())
                else:
                    dx.insertintoDB('monopoly_game_db', "INSERT INTO utilities values (%d, %d, %d)" % i.state())
            
            for i in self.Banker.accounts:
                dx.insertintoDB('monopoly_game_db', "INSERT INTO accounts values (%d, %d, %d)" % i.acc_state())
            self.logObj.printer("Current game saved into database.")
        except ValueError:
            self.logObj.printer("Unable to log into the database.")


    def set_owner_in_asset(self, board_pos, plid):
        if plid > 0:
            if plid > 10: plid -= 10
            assets_board_locations[board_pos] =  Smartcontroller.color_code[plid] + "|P%d|" % plid + color_coded[8]

    def setprevgame(self):
        try:
            dx = DBhandler(self.dbuser, self.dbpassword) 
            x = dx.queryDB('monopoly_game_db', 'SELECT * from countries')
            for i in x:
                self.Banker.get_asset_by_assetid(i[0]).change_state((i[1], i[2], i[3], bool(i[4]), bool(i[5])))
                self.set_owner_in_asset(i[0], i[1])
                
            x = dx.queryDB('monopoly_game_db', 'SELECT * from utilities')
            for i in x:
                self.Banker.get_asset_by_assetid(i[0]).change_state((i[1], i[2]))
                self.set_owner_in_asset(i[0], i[1])
                
            x = dx.queryDB('monopoly_game_db', 'SELECT * from player')
            for i in x:
                self.players.append(Smartplayer(i[0], i[1], self.logPath)) 
                if i[4] == 1:
                    self.available_players_id.append(i[0])
                if i[5] > 0:
                    self.turnHolderPlayerID = i[0]
                self.players[i[0]-1].change_state((bool(i[2]), i[3]))                        
            self.Banker.add_players_accounts(self.player_count, 'a')
            x = dx.queryDB('monopoly_game_db', 'SELECT * from accounts')
            for i in x:
                self.Banker.accounts[i[0]].change_state((i[1], bool(i[2])))
            dx.dropDB('monopoly_game_db')
        except:
            self.logObj.printer('Error while reading the previous game from DB.')    
