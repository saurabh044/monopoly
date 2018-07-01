from MenuBox import Printer
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
    
    def deactivate(self):
        self.active = False
        self.board_pos = 0
        
    def state(self):
        return (self.id, self.name, self.active, self.board_pos) 
    
    def change_state(self, new_state):
        (self.active, self.board_pos) = new_state
        
