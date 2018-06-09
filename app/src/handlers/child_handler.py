from commandbus import Command, CommandHandler
import json
import psycopg2

class ChildHandler(CommandHandler):
    """Handle child command"""

    def handle(self, ChildCommand: Command):

        # Child command only available in normal mode
        if ChildCommand.mode == 'normal':
            with ChildCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            ChildCommand.params['admin'],
                            ChildCommand.params['passwd']))

                    cur.callproc('child', (
                            ChildCommand.params['emp'],))
                    
                    children = [child[0] for child in cur.fetchall()]
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': children}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
