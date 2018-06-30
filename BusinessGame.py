from Smartcontroller import Smartcontroller
from MenuBox import MenuBox, Printer
import os
from cmdbtester import DBhandler

if not os.path.exists("business_game_logs"):
    os.makedirs("business_game_logs")
logPath = "./business_game_logs/business.logs"
fH = open(logPath, 'w')
fH.close()
p = Printer(logPath)
dbuser = raw_input("Enter the username for MySQL DB (default root): ")
if dbuser == "":
    dbuser = 'root'
dbpassword = raw_input("Enter the password for MySQL DB (default root): ")
if dbpassword == "":
    dbpassword = 'root'
dx = None
try:
    dx = DBhandler(dbuser, dbpassword)
except:
    p.printer("Connection failed to MySQL server. You will not be able to save the ongoing game for later.")
# initial Game Start Menu
gameretrieve = MenuBox("MONOPOLY GAME", logPath)
if dx is not None:
    gameretrieve.addOptions(["Retrieve saved game", "New Game"])
    optionRecv = 4
    option = gameretrieve.runMenu()
    if option == 1:
        dx = DBhandler(dbuser, dbpassword)
        if dx.isDBexist('monopoly_game_db') == 1:
            x = dx.queryDB('monopoly_game_db', 'SELECT count(*) from player')
            players_count = x[0][0]
            x = dx.queryDB('monopoly_game_db', 'select isturnholder from player where isturnholder > 0')
            chanceCount = x[0][0]
            GameController = Smartcontroller(players_count, logPath, dbuser, dbpassword)
            GameController.setprevgame() 
            optionRecv = 5 - players_count
        else:
            p.printer("Unable to retrieve any saved game.") 
    elif option == 2:
        gameStartMenu = MenuBox("Start Game:", logPath)
        gameStartMenu.addOptions(["4 Player ", "3 Player ", "2 Player "])
        optionRecv = gameStartMenu.runMenu()
        if optionRecv != 4:
            chanceCount = 0    
            GameController = Smartcontroller(5-optionRecv, logPath, dbuser, dbpassword)
            GameController.addplayersingame()
    else:
        p.printer("Exiting.") 
else:
    gameStartMenu = MenuBox("Start Game:", logPath)
    gameStartMenu.addOptions(["4 Player ", "3 Player ", "2 Player "])
    optionRecv = gameStartMenu.runMenu()
    if optionRecv != 4:
        chanceCount = 0    
        GameController = Smartcontroller(5-optionRecv, logPath)
        GameController.addplayersingame()   
if optionRecv != 4:
    optionGameRecv = GameController.state
    GameController.display_board()
    GameController.print_all_player_assets_table()
    try:
        while optionGameRecv:
            chanceCount += 1
            GameController.next_move(chanceCount)
            optionGameRecv = GameController.state
    except KeyboardInterrupt:
        p.printer("\nYou ended the game abruptly and couldn't be saved.")
else:
    p.printer("Exiting the game.")    
