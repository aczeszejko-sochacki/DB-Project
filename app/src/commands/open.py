from commandbus import Command

class OpenCommand(Command):
    """Create open command"""

    def __init__(self, params):
        self.params = params

