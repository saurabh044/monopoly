def p(inp):
    print inp
    mx = max(inp)
    y = [True if i == mx and mx != 0 else False for i in inp]
    print y
    
    

l = [4, 5, 10, 15]
print l
for i in l:
    if i == 5:
        i += 1
print l 



def set_turn(ind, turnHolderPlayerID, value, maxkeynum):
    x = False
    while x == False:
        check_key = (value + turnHolderPlayerID) % (maxkeynum + 1)
        if check_key in ind.keys():
            x = True
            turnHolderPlayerID = check_key
        else:
            if value < 0:
                value -= 1
            else:
                value += 1
    return turnHolderPlayerID

available_players_index = {1: 0, 2: 1, 3: 2, 4: 3}
turnHolderPlayerID = 0 
turn_val = 0 
for i in range(20):      
    turn_val = set_turn(available_players_index, turn_val, 1, 4)
    print "New Holder = %d " % turn_val  
            
print 
print          
 
available_players_index = {1: 0, 2: 1, 3: 2, 4: 3}
turnHolderPlayerID = 0 
turn_val = 0 
for i in range(20):      
    turn_val = set_turn(available_players_index, turn_val, -1, 4)
    print "New Holder = %d " % turn_val  
print 
print          
            
available_players_index = {1: 0, 4: 3}
turnHolderPlayerID = 0 
turn_val = 0 
for i in range(20):      
    turn_val = set_turn(available_players_index, turn_val, 1, 4)
    print "New Holder = %d " % turn_val 
    
print 
print  

available_players_index = {1: 0, 2: 1, 3: 2}
turnHolderPlayerID = 0 
turn_val = 0 
for i in range(20):      
    turn_val = set_turn(available_players_index, turn_val, -1, 4)
    print "New Holder = %d " % turn_val  
print 
print  

available_players_index = {1: 0, 2: 1, 4: 3}
turnHolderPlayerID = 0 
turn_val = 0 
for i in range(20):      
    turn_val = set_turn(available_players_index, turn_val, 1, 4)
    print "New Holder = %d " % turn_val  
print 
print             
 