from commandbus import Command

class NewCommand(Command):
    """Create new command"""

    def __init__(self, db_conn, params):
        self.db_conn = db_conn
        self.params = params

