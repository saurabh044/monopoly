from Smartcontroller import Smartcontroller
from MenuBox import MenuBox, Printer, DBhandler, color_coded
from colorama import init, Fore, Back, Style
import os


if not os.path.exists("business_game_logs"): os.makedirs("business_game_logs")
logPath = "./business_game_logs/business.logs"
p = Printer(logPath)
try:
    dbuser = raw_input(color_coded[11] + "Enter the username for MySQL DB (default root): " + color_coded[8])
    if dbuser == "": dbuser = 'root'
    dbpassword = raw_input(color_coded[11] +"Enter the password for MySQL DB (default root): " + color_coded[8])
    if dbpassword == "": dbpassword = 'root'
    dx = None
    try:
        dx = DBhandler(dbuser, dbpassword)
    except:
        p.printer(color_coded[10] + "Connection failed to MySQL server. You will not be able to save the ongoing game for later." + color_coded[8])
    gameretrieve = MenuBox("MONOPOLY GAME", logPath)
    gameStartMenu = MenuBox("Start Game:", logPath)
    gameStartMenu.addOptions(["4 Player ", "3 Player ", "2 Player "])
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
                with open(logPath, 'a') as fH: pass
                GameController = Smartcontroller(players_count, logPath, dbuser, dbpassword)
                GameController.setprevgame() 
                optionRecv = 5 - players_count
            else:
                p.printer(color_coded[10] + "Unable to retrieve any saved game." + color_coded[8]) 
        elif option == 2:
            with open(logPath, 'w') as fH: pass
            optionRecv = gameStartMenu.runMenu()
            if optionRecv != 4:
                chanceCount = 0    
                GameController = Smartcontroller(5-optionRecv, logPath, dbuser, dbpassword)
                GameController.addplayersingame()
        else:
            p.printer("Exiting.") 
    else:
        with open(logPath, 'w') as fH: pass
        try:
            optionRecv = gameStartMenu.runMenu()
        except KeyboardInterrupt:
            p.printer(color_coded[10] + "\nYou ended the game abruptly." + color_coded[8])
        if optionRecv != 4:
            chanceCount = 0    
            GameController = Smartcontroller(5-optionRecv, logPath)
            GameController.addplayersingame()   
    if optionRecv != 4:
        optionGameRecv = GameController.state
        try:
            while optionGameRecv:
                chanceCount += 1
                GameController.next_move(chanceCount)
                optionGameRecv = GameController.state
        except KeyboardInterrupt:
            p.printer(color_coded[10] + "\n\nYou ended the game abruptly and couldn't be saved." + color_coded[8])
    else:
        p.printer(color_coded[11] + "Exiting the game." + color_coded[8])    
except KeyboardInterrupt:
    p.printer(color_coded[10] + "\n\nYou ended the game abruptly." + color_coded[8]) 
