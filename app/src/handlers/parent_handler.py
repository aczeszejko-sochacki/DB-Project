from commandbus import Command, CommandHandler
import json
import psycopg2

class ParentHandler(CommandHandler):
    """Handle parent command"""

    def handle(self, ParentCommand: Command):
        
        # Parent command only available in normal mode
        if ParentCommand.mode == 'normal':
            with ParentCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            ParentCommand.params['admin'],
                            ParentCommand.params['passwd']))

                    cur.callproc('parent', (
                            ParentCommand.params['emp'],))

                    parent = cur.fetchone()[0]
                    print(json.JSONEncoder().encode(
                        {'status': 'OK', 'data': parent}))

                except psycopg2.DatabaseError:

                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
