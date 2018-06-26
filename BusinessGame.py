from Smartcontroller import Smartcontroller
from MenuBox import MenuBox
from Printer import Printer
import os
if not os.path.exists("business_game_logs"):
    os.makedirs("business_game_logs")
logPath = "./business_game_logs/business.logs"
fH = open(logPath, 'w')
fH.close()
p = Printer(logPath)
# initial Game Start Menu
gameStartMenu = MenuBox("Start Game:", logPath)
gameStartMenu.addOption("Two Player ")
gameStartMenu.addOption("Three Player ")
gameStartMenu.addOption("Four Player ")
optionRecv = gameStartMenu.auto_runMenu(3) # simulation
#optionRecv = 3 # simulation line

if optionRecv != 4:
    GameController = Smartcontroller(optionRecv+1, logPath)
    optionGameRecv = GameController.state
    chanceCount = 0    
    while optionGameRecv:
        GameController.display_board()
        GameController.print_all_player_assets_table()
        chanceCount += 1
        GameController.next_move(chanceCount)
        optionGameRecv = GameController.state
else:
    p.printer("Exiting.")  

