from commandbus import Command

class NewCommand(Command):
    """Create new command"""

    def __init__(self, db_conn, params, mode):
        self.db_conn = db_conn
        self.params = params

