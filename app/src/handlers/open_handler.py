from commandbus import Command, CommandHandler
import json
import psycopg2
import sys

class OpenHandler(CommandHandler):
    """Handle open command"""

    def handle(self, OpenCommand: Command):
        command_name = list(OpenCommand.params.keys())[0]
        db_params = list(OpenCommand.params.values())[0]

        if command_name != 'open':
            # Expected 'open' command
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
            sys.exit(1)

        # Check connection with the specified database
        try:
            with psycopg2.connect(host='localhost',
                                dbname=db_params['database'],
                                user=db_params['user'],
                                password=db_params['password']) \
                            as db_conn:
                
                # Connected to database
                print(json.JSONEncoder().encode({'status': 'OK'}))

        except psycopg2.DatabaseError:
            # Connection failed, stop execution
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
            sys.exit(1)
