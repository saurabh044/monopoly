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
gameretrieve = MenuBox("MONOPOLY GAME", logPath)
gameretrieve.addOptions(["Retrieve saved game", "New Game"])
option = gameretrieve.runMenu()
if option == 1:
    pass
elif option == 2:
    gameStartMenu = MenuBox("Start Game:", logPath)
    gameStartMenu.addOptions(["4 Player ", "3 Player ", "2 Player "])
    optionRecv = gameStartMenu.runMenu()
    if optionRecv != 4:
        GameController = Smartcontroller(5-optionRecv, logPath)
        GameController.db_populate()
        optionGameRecv = GameController.state
        chanceCount = 0    
        GameController.display_board()
        GameController.print_all_player_assets_table()
        try:
            while optionGameRecv:
                chanceCount += 1
                GameController.next_move(chanceCount)
                optionGameRecv = GameController.state
        except KeyboardInterrupt:
            p.printer("\nYou ended the game abruptly. Game Drawn.")
    else:
        p.printer("Exiting.")  
else:
    p.printer("Exiting.")
    
