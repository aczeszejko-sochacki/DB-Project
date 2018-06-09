from commandbus import Command

class ReadCommand(Command):
    """Create read command"""

    def __init__(self, db_conn, params, mode):
        self.db_conn = db_conn
        self.params = params
        self.mode = mode
