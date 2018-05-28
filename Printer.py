class Printer(object):

    def __init__(self, filename=""):
        self.LogFileName = filename

    def printer(self, inp_text):
        print inp_text
        fh = open(self.LogFileName, 'a')
        fh.write("%s\n" % inp_text)
        fh.close()

    def file_only_printer(self, inp_text):
        fh = open(self.LogFileName, 'a')
        fh.write("%s\n" % inp_text)
        fh.close()

    def set_log_file_name(self, filename):
        self.LogFileName = filename
        fh = open(self.LogFileName, 'w')
        fh.close()
