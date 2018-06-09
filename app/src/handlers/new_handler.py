from commandbus import Command, CommandHandler
import json
import psycopg2

class NewHandler(CommandHandler):
    """ Handle new command"""

    def handle(self, NewCommand: Command):
        with NewCommand.db_conn.cursor() as cur:

            # Attempt to commit transaction
            try:
                cur.callproc('check_password', (
                        NewCommand.params['admin'],
                        NewCommand.params['passwd']))

                cur.callproc('ancestor_or_equal', (
                        NewCommand.params['emp1'],
                        NewCommand.params['admin']))

                cur.callproc('insert_new_worker', (
                        NewCommand.params['emp'],
                        NewCommand.params['newpasswd'],
                        NewCommand.params['emp1'],
                        NewCommand.params['data']))

                NewCommand.db_conn.commit()

                print(json.JSONEncoder().encode({'status': 'OK'}))

            except psycopg2.DatabaseError:

                # Transaction failed
                NewCommand.db_conn.rollback()
                print(json.JSONEncoder().encode({'status': 'ERROR'}))

