from commandbus import Command, CommandHandler

class NewHandler(CommandHandler):
    """ Handle new command"""

    def handle(self, NewCommand: Command):
        with NewCommand.db_conn.cursor() as cur:

            # Return status of transaction
            return cur.callproc('new', (
                        NewCommand.params['emp'],
                        NewCommand.params['newpasswd'],
                        NewCommand.params['emp1'],
                        NewCommand.params['data']))

