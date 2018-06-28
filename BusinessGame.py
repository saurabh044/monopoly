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
gameStartMenu.addOptions(["2 Player ", "3 Player ", "4 Player "])
optionRecv = gameStartMenu.runMenu() # simulation
#optionRecv = 3 # simulation line
if optionRecv != 4:
    GameController = Smartcontroller(optionRecv+1, logPath)
    optionGameRecv = GameController.state
    chanceCount = 0    
    try:
        while optionGameRecv:
            GameController.display_board()
            GameController.print_all_player_assets_table()
            chanceCount += 1
            GameController.next_move(chanceCount)
            optionGameRecv = GameController.state
    except KeyboardInterrupt:
        p.printer("\nYou ended the game abruptly. Game Drawn.")
else:
    p.printer("Exiting.")  

