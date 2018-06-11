from commandbus import Command, CommandHandler
import json
import psycopg2

class DescendantsHandler(CommandHandler):
    """Handle descendants command"""

    def handle(self, DescendantsCommand: Command):

        # Descendants command only available in normal mode
        if DescendantsCommand.mode == 'normal':
            with DescendantsCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            DescendantsCommand.params['admin'],
                            DescendantsCommand.params['passwd']))

                    cur.callproc('descendants', (
                            DescendantsCommand.params['emp'],))
                    
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': 
                            [anc[0] for anc in cur.fetchall()]}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
