from Printer import Printer
class Smartplayer(object):
    
    def __init__(self, id, name, logPath, active=True):
        self.id = id
        self.name = name
        self.active = active
        self.logObj = Printer(logPath)
        self.board_pos = 1
        self.transaction_statement = Printer()
        self.asset_counter = {'Ro': 0, 'Go': 0, 'Bo': 0, 'Yo': 0, 'U1o': 0,
                              'Rm': 0, 'Gm': 0, 'Bm': 0, 'Ym': 0, 'Um': 0} 
        self.assets_name = {}
        
    def set_statement_filename(self, fname):
        self.transaction_statement.set_log_file_name(fname)
        self.transaction_statement.file_only_printer("{: >60} {: >8} {: >8} {: >8}".format("Transaction Details",
                                                                                           "Debit", "Credit", "Balance"))
    
    def move(self, value):
        self.board_pos += value
        if self.board_pos > 36:
            self.board_pos -= 36
            return True
        return False
    
    def jump(self, value):
        self.board_pos = value
            
    def deactivate(self):
        self.active = False
    