from commandbus import Command, CommandHandler
import json
import psycopg2

class AncestorHandler(CommandHandler):
    """Handle ancestor command"""

    def handle(self, AncestorCommand: Command):

        # Ancestor command only available in normal mode
        if AncestorCommand.mode == 'normal':
            with AncestorCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            AncestorCommand.params['admin'],
                            AncestorCommand.params['passwd']))


                    cur.callproc('ancestor', (
                            AncestorCommand.params['emp1'],
                            AncestorCommand.params['emp2']))
                    
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': cur.fetchone()[0]}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
