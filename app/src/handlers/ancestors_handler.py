from commandbus import Command, CommandHandler
import json
import psycopg2

class AncestorsHandler(CommandHandler):
    """Handle ancestors command"""

    def handle(self, AncestorsCommand: Command):

        # Ancestors command only available in normal mode
        if AncestorsCommand.mode == 'normal':
            with AncestorsCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            AncestorsCommand.params['admin'],
                            AncestorsCommand.params['passwd']))

                    cur.callproc('ancestors', (
                            AncestorsCommand.params['emp'],))
                    
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': 
                            [anc[0] for anc in cur.fetchall()]}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
