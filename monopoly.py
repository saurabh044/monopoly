from Controller import Controller
from MenuBox import MenuBox
from Dice import Dice
from Printer import Printer
import os
if not os.path.exists("game_logs"):
    os.makedirs("game_logs")
logPath = "./game_logs/monopoly.logs"
fH = open(logPath, 'w')
fH.close()
p = Printer(logPath)
# initial Game Start Menu
gameStartMenu = MenuBox("Start Game:", logPath)
gameStartMenu.addOption("Two Player ")
gameStartMenu.addOption("Three Player ")
gameStartMenu.addOption("Four Player ")
optionRecv = gameStartMenu.runMenu()


if optionRecv != 4:
    GameController = Controller(optionRecv+1, logPath)
    GameController.set_turnHolderPlayerID(1)
    Dice1 = Dice()
    GameController.get_players_name()
    GameController.add_players_in_game()
    GameController.add_countries_in_game()
    GameController.give_initial_money_to_player()

    gamePlayMenu = MenuBox("Play Game", logPath)
    gamePlayMenu.addOption("Roll Dice")

    PlayerMenu = MenuBox("Player Menu", logPath)
    PlayerMenu.addOption("Continue")
    PlayerMenu.addOption("Redeem")
    PlayerMenu.addOption("Build Property")
    PlayerMenu.addOption("Sell Property")
    PlayerMenu.addOption("Buy Other Player Country")
    PlayerMenu.addOption("Mortgage")

    PlayerBuyMenu = MenuBox("Buy Menu", logPath)
    PlayerBuyMenu.addOption("Want to buy")

    optionGameRecv = 0
    chanceCount = 0
    while optionGameRecv != 2:
        playerTurn = GameController.get_turnHolderPlayerID()
        GameController.set_game_state(1)
        GameController.display_board()
        GameController.print_all_player_assets_table()
        chanceCount += 1
        p.printer("Chance #%d" % chanceCount)
        p.printer("Player %s, your chance" % GameController.get_player_name_by_its_ID(playerTurn))
        optionGameRecv = gamePlayMenu.auto_runMenu(1)  # This auto_runMenu statement is for simulation purpose.
        if optionGameRecv == 1:
            dice_out = Dice1.throw_dice()
            p.printer("Dice outcome = %d" % dice_out)
            isCrossover = GameController.get_player_by_its_ID(playerTurn).move_me(dice_out)
            if isCrossover:
                GameController.player_payment_on_crossover(playerTurn)
            GameController.print_movement_info(playerTurn)
            ownerID = GameController.get_property_owner_where_player_standing(playerTurn)
            if ownerID == -1:
                player_pos = GameController.get_board_position_where_player_standing(playerTurn)
                if player_pos == 5 or player_pos == 26:  # UNO
                    GameController.apply_uno_to_player(playerTurn, dice_out)
                elif player_pos == 17 or player_pos == 30:  # CHANCE
                    GameController.apply_chance_to_player(playerTurn, dice_out)
                elif player_pos == 14:  # custom duty
                    GameController.payCustomDuty(playerTurn)
                elif player_pos == 22:  # travelling duty
                    GameController.payTravellingDuty(playerTurn)
                elif player_pos == 28:  # JAIL
                    GameController.gotojail(playerTurn)
                elif player_pos == 10:  # Resort
                    GameController.enjoyment_in_resort(playerTurn)
                elif player_pos == 19:  # Party House
                    GameController.get_party_from_others(playerTurn)
                else:
                    pass
            else:
                if GameController.check_property_availability_status(playerTurn):
                    if GameController.check_player_ability_to_buy_property(playerTurn):
                        player_buyconsent = PlayerBuyMenu.auto_runMenu(1)  # This auto_runMenu statement is for simulation purpose.
                        if player_buyconsent == 1:
                            p.printer("Purchase Done.")
                            GameController.sell_property_to_player(playerTurn)
                        else:
                            p.printer("Player-%d is not interested in this property." % playerTurn)
                    else:
                        p.printer("Player-%d doesn't have sufficient cash to buy this property." % playerTurn)
                elif ownerID == playerTurn:
                    p.printer("You reached on your own property.")
                    pass
                elif 0 < ownerID < 5:
                    amnt = GameController.get_property_rent_where_player_standing(playerTurn)
                    GameController.transaction_between_two_player(ownerID, playerTurn, amnt)
                    p.printer("This is Player%d's property. The rent of amount $%s needs to be paid." % (ownerID, amnt))
                else:
                    pass

            GameController.check_players_with_negative_cash()
            BankCashCheck = GameController.check_bank_with_negative_cash(0)
            GameController.display_board()
            GameController.print_all_player_assets_table()
            if GameController.get_game_state() == 1:
                optionPlayerRecv = 0
                while optionPlayerRecv != 1:
                    if chanceCount < 500:
                        optionPlayerRecv = PlayerMenu.auto_runMenu(1)
                    else:
                        optionPlayerRecv = PlayerMenu.runMenu()
                    if optionPlayerRecv == 1:
                        p.printer("Continuing the game...\n")
                    elif optionPlayerRecv == 2:
                        p.printer("Player %d wants to redeem his mortgaged assets" % GameController.get_turnHolderPlayerID())
                        GameController.redeem_mortgaged_property_of_player(GameController.get_turnHolderPlayerID())
                    elif optionPlayerRecv == 3:
                        p.printer("Player %d wants to build property on his site" % GameController.get_turnHolderPlayerID())
                        GameController.build_property_on_player_site(GameController.get_turnHolderPlayerID())
                    else:
                        pass
                GameController.move_turnHolderPlayerID()
            elif GameController.get_game_state() == -1:
                p.printer("Game Finished and the winner is %s.\n" % GameController.get_winner_name())
                optionGameRecv = 2
            elif GameController.get_game_state() == -2:
                p.printer("Game drawn due to bank ran out of cash after %d chances.\n" % chanceCount)
                winnerID = GameController.get_winner()
                winnerName = GameController.get_player_name_by_its_ID(winnerID)
                p.printer("The winner is Player-%d, %s!" % (winnerID, winnerName))
                optionGameRecv = 2
            else:
                pass
else:
    p.printer("Exiting.")

