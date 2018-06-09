from commandbus import Command, CommandHandler
import json
import psycopg2

class UpdateHandler(CommandHandler):
    """Handle update command"""

    def handle(self, UpdateCommand: Command):
        
        # Update command only available in normal mode
        if UpdateCommand.mode == 'normal':
            with UpdateCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            UpdateCommand.params['admin'],
                            UpdateCommand.params['passwd']))

                    cur.callproc('ancestor_or_equal', (
                            UpdateCommand.params['emp'],
                            UpdateCommand.params['admin']))

                    cur.callproc('update', (
                            UpdateCommand.params['emp'],
                            UpdateCommand.params['newdata']))
                    
                    print(json.JSONEncoder().encode({'status': 'OK'}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
