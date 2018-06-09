from commandbus import Command, CommandHandler
import json
import psycopg2

class ReadHandler(CommandHandler):
    """Handle read command"""

    def handle(self, ReadCommand: Command):
        
        # Read command only available in normal mode
        if ReadCommand.mode == 'normal':
            with ReadCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            ReadCommand.params['admin'],
                            ReadCommand.params['passwd']))

                    cur.callproc('ancestor_or_equal', (
                            ReadCommand.params['emp'],
                            ReadCommand.params['admin']))

                    cur.callproc('read', (
                            ReadCommand.params['emp'],))

                    data = cur.fetchone()[0]
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': data}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
