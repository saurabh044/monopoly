from cmdbtester import DBhandler

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
# key value array of Utility (boardPosition, buyValue, mortgageValue, rent, pair_rent, group_id)
utility_list = {"Waterways": (4, 9500, 2000, 1400, 2200, 1),
                "Satellite": (8, 2000, 1250, 500, 1000, 1),
                "Airways": (13, 10500, 5500, 1500, 2500, 3),
                "Roadways": (23, 3500, 1800, 800, 1500, 2),
                "Petroleum": (32, 5500, 1300, 500, 1000, 3),
                "Railways": (34, 9500, 5000, 1500, 2500, 2)
                }

board_display_data = ("Start", "England R-2500", "Iraq G-5000", 
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
                      "Singapore B-3000")
assets_board_locations = { 2: "",  3: "",  4: "",  6: "",
                           7: "",  8: "",  9: "", 11: "",
                          12: "", 13: "", 15: "", 16: "",
                          18: "", 20: "", 21: "", 23: "",
                          24: "", 25: "", 27: "", 29: "",
                          31: "", 32: "", 33: "", 34: "",
                          35: "", 36: ""}

dx = DBhandler(username='root', password='root')
if dx.isDBexist('monopoly') == -1:
    dx.createDB("monopoly")
    dx.createTable('monopoly', 'countries', ['name', 'boardposition', 'buyvalue',
                                             'mortgagevalue', 'colorgroup', 
                                             'basicrent', 'property_price',
                                             'property_rent'], ['varchar(20)', 
                                                                'int primary key',
                                                              'int', 'int', 'int',
                                                              'int', 'int', 'int'])
    
    dx.createTable('monopoly', 'utilities', ['name', 'boardposition', 'buyvalue',
                                             'mortgagevalue', 'rent', 'pair_rent', 
                                             'group_id'], ['varchar(20)', 
                                                           'int primary key',
                                                            'int', 'int', 'int',
                                                            'int', 'int']) 
    dx.createTable('monopoly', 'positionname', ['boardposition', 'name', 'isasset'], 
                                                ['int primary key', 'varchar(30)', 
                                                 'tinyint'])
    
    for i in country_list.keys():
        dx.insertintoDB('monopoly', "INSERT INTO countries values (\'%s\', %d," \
                             "%d, %d, %d, %d, %d, %d)" % ((i,) + country_list[i]))                    
    for i in utility_list.keys():
        dx.insertintoDB('monopoly', "INSERT INTO utilities values (\'%s\', %d," \
                             "%d, %d, %d, %d, %d)" % ((i,) + utility_list[i]))
     
    for i in range(36):
        isasset = 0
        if (i+1) in assets_board_locations: isasset = 1
        dx.insertintoDB('monopoly', "INSERT INTO positionname values (%d, \'%s\', %d)" 
                        % (i+1, board_display_data[i], isasset))
        
    
