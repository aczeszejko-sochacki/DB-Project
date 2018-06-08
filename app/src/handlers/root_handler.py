from commandbus import Command, CommandHandler

class RootHandler(CommandHandler):
    """Handle root command"""

    def handle(self, RootCommand: Command):

        # root command only available in init mode
        if RootCommand.mode == 'init':
            with RootCommand.db_conn.cursor() as cur:
                
                # root has not a supervisor
                if RootCommand.params['secret'] != 'qwerty':
                    pass    # return fail; to do

                cur.execute('''INSERT INTO workers(emp, password, data)
                    VALUES (%s, %s, %s)''', (
                            RootCommand.params['emp'],
                            RootCommand.params['newpassword'],
                            RootCommand.params['data']))

        else:
            pass    # return fail; to do
