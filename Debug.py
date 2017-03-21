

class Debug:
    def __init__(self, setup):
        self.verbose = setup.verbose

    def print_commum(self, msg):
        if self.verbose:
            print msg
