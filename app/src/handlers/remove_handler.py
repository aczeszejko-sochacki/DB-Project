from commandbus import Command, CommandHandler
import json
import psycopg2

class RemoveHandler(CommandHandler):
    """Handle remove command"""

    def handle(self, RemoveCommand: Command):

        # Remove command only available in normal mode
        if RemoveCommand.mode == 'normal':
            with RemoveCommand.db_conn.cursor() as cur:

                # Transaction
                try:
                    cur.callproc('check_password', (
                            RemoveCommand.params['admin'],
                            RemoveCommand.params['passwd']))

                    cur.callproc('ancestor_not_equal', (
                            RemoveCommand.params['emp'],
                            RemoveCommand.params['admin']))

                    cur.callproc('remove', (
                            RemoveCommand.params['emp'],))
                    
                    print(json.JSONEncoder().encode(
                        {'status': 'OK'}))

                except psycopg2.DatabaseError:
                    # Transaction failed
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))
        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
