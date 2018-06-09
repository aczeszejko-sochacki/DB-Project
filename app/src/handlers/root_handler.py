from commandbus import Command, CommandHandler

class RootHandler(CommandHandler):
    """Handle root command"""

    def handle(self, RootCommand: Command):

        # Root command only available in init mode
        if RootCommand.mode == 'init':
            with RootCommand.db_conn.cursor() as cur:
                
                # Root has not a supervisor
                if RootCommand.params['secret'] != 'qwerty':
                    return False    # to do
                
                # Return status of transaction
                return cur.callproc('root', (
                            RootCommand.params['emp'],
                            RootCommand.params['newpassword'],
                            RootCommand.params['data']))

        else:
            # Transaction failed
            return False    
