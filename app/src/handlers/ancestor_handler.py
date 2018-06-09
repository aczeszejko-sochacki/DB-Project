from commandbus import Command, CommandHandler

class AncestorHandler(CommandHandler):
    """ Handle ancestor command"""

    def handle(self, AncestorCommand: Command):
        with AncestorCommand.db_conn.cursor() as cur:

            # Ancestor only in normal mode
            if AncestorCommand == 'normal':
                
                # Return status of transaction
                return cur.callproc('ancestor', (
                    AncestorCommand.params['emp1'],
                    AncestorCommand.params['emp2']))
            else:
                # Transaction failed
                return False    # to do
