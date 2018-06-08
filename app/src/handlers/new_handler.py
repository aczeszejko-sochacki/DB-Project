from commandbus import Command, CommandHandler

class NewHandler(CommandHandler):
    """ Handle new command"""

    def handle(self, NewCommand: Command):
        with NewCommand.db_conn.cursor() as cur:
            cur.execute('''INSERT INTO workers 
                    VALUES(%s, %s, %s, %s)''', (
                        NewCommand.params['emp'],
                        NewCommand.params['newpasswd'],
                        NewCommand.params['emp1'],
                        NewCommand.params['data']))

