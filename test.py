from Banksmart import Banksmart, Transaction
from Asset import Country, Utility
from Smartplayer import Smartplayer
logPath = "./business_game_logs/businesstest.logs"
b = Banksmart(0, logPath)
b.add_players_accounts(4)
b.process_request(Transaction(-1, 0, 12, 10000000, "Cash reserved to bank"))
# Initial payment of $25000 to all the players for starting the game 
for i in range(4):
    b.process_request(Transaction(0, i+1, 11, 1000000, "Initial Payment"))


country_list = {"England":   [ 2, 7000, 3500, 1, 700, 7000, 1700],
                "France":    [ 6, 2500, 1250, 1, 300, 2500, 1300],
                "Germany":   [12, 3500, 1750, 1, 400, 3500, 1400],
                "Swiss":     [15, 3500, 3300, 1, 700, 6500, 1700],
                "Italy":     [18, 3500, 1000, 1, 200, 2000, 1200],
                "Iraq":      [ 3, 5000, 2500, 2, 500, 5000, 1500],
                "Iran":      [ 7, 2500, 1250, 2, 300, 2500, 1300],
                "Egypt":     [ 9, 3200, 1500, 2, 300, 3200, 1300],
                "Malaysia":  [35, 1500,  800, 2, 200, 1500, 1200],
                "SaudiArab": [31, 5500, 2800, 2, 600, 5500, 1600],
                "India":     [29, 5500, 2750, 3, 550, 5500, 1550],
                "China":     [33, 4500, 2250, 3, 450, 4500, 1450],
                "Singapore": [36, 3000, 1500, 3, 300, 3000, 1300],
                "Japan":     [20, 2500, 1250, 3, 250, 2500, 1250],
                "Hongkong":  [25, 2000, 1000, 3, 200, 2500, 1200],
                "Canada":    [11, 4000, 2000, 4, 400, 4000, 1400],
                "Brazil":    [16, 2500, 1300, 4, 300, 2500, 1300],
                "USA":       [21, 8500, 5000, 4, 1000, 8500, 2000],
                "Mexico":    [24, 4000, 2000, 4, 900, 4000, 1800],
                "Australia": [27, 3300, 2000, 4, 400, 3300, 1400]
                }
# key value array of Utility [boardPosition, buyValue, mortgageValue, rent, pair_rent, group_id]
utility_list = {"Waterways": [4, 9500, 2000, 1400, 2200, 1],
                "Satellite": [8, 2000, 1250, 500, 1000, 1],
                "Roadways": [23, 3500, 1800, 800, 1500, 2],
                "Railways": [34, 9500, 5000, 1500, 2500, 2],
                "Petroleum": [32, 5500, 1300, 500, 1000, 3],
                "Airways": [13, 10500, 5500, 1500, 2500, 3]
                }

for i in country_list:
    b.asset_list.append(Country(country_list[i][0], i,
                                     country_list[i][1],
                                     country_list[i][2],
                                     country_list[i][4],
                                     country_list[i][5],
                                     country_list[i][6],
                                     country_list[i][3]))
for i in utility_list:
    b.asset_list.append(Utility(utility_list[i][0], i, 
                                     utility_list[i][1], 
                                     utility_list[i][2], 
                                     utility_list[i][3], 
                                     utility_list[i][4],
                                     utility_list[i][5]))

def print_asset():
    print "current site list\n-----------------"
    for c in range(1,5):
        for i in b.asset_list:
            if i.issite():
                if i.color_grp == c:
                    print i
        print 

b.sell_asset_to_player(1, 2)
print_asset()

b.sell_asset_to_player(1, 6)
print_asset()

b.sell_asset_to_player(1, 12)
print_asset()

b.sell_asset_to_player(1, 15)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_building_to_player(1,6)
print_asset()

b.sell_building_to_player(1,12)
print_asset()

b.sell_building_to_player(1,15)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_building_to_player(1,6)
print_asset()

b.sell_building_to_player(1,12)
print_asset()

b.sell_building_to_player(1,15)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_building_to_player(1,6)
print_asset()

b.sell_building_to_player(1,12)
print_asset()

b.sell_building_to_player(1,15)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_building_to_player(1,6)
print_asset()

b.sell_building_to_player(1,12)
print_asset()

b.sell_building_to_player(1,15)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_asset_to_player(1, 18)
print_asset()

b.sell_building_to_player(1,18)
print_asset()

b.sell_building_to_player(1,18)
print_asset()
b.sell_building_to_player(1,18)
print_asset()
b.sell_building_to_player(1,18)
print_asset()
b.sell_building_to_player(1,18)
print_asset()

b.get_building_from_player(1,12)
print_asset()
b.get_building_from_player(1,2)
print_asset()
b.get_building_from_player(1,6)
print_asset()
b.get_building_from_player(1,15)
print_asset()
b.get_building_from_player(1,18)
print_asset()

b.get_building_from_player(1,12)
print_asset()
b.get_building_from_player(1,2)
print_asset()
b.get_building_from_player(1,6)
print_asset()
b.get_building_from_player(1,15)
print_asset()
b.get_building_from_player(1,18)
print_asset()
b.get_building_from_player(1,12)
print_asset()
b.get_building_from_player(1,2)
print_asset()
b.get_building_from_player(1,6)
print_asset()
b.get_building_from_player(1,15)
print_asset()
b.get_building_from_player(1,18)
print_asset()

b.get_building_from_player(1,12)
print_asset()
b.get_building_from_player(1,2)
print_asset()
b.get_building_from_player(1,6)
print_asset()
b.get_building_from_player(1,15)
print_asset()
b.get_building_from_player(1,18)
print_asset()

b.get_building_from_player(1,12)
print_asset()

b.sell_building_to_player(1,2)
print_asset()

b.sell_building_to_player(1,6)
print_asset()

b.sell_building_to_player(1,12)
print_asset()

b.sell_building_to_player(1,15)
print_asset()

b.sell_building_to_player(1,18)
print_asset()







