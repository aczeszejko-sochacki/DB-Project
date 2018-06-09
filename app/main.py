import psycopg2
import json
from commandbus import Command, CommandHandler, CommandBus
from init import init_db
from src import read_data
from src import RootCommand
from src import NewCommand
from src import AncestorCommand
from src import RootHandler
from src import NewHandler
from src import AncestorHandler

def main():
    """
    Main. Init database, create command bus, 
    receive commands and pass to handlers
    """

    # Init commandbus and handlers
    bus = CommandBus()
    root_handler = RootHandler()
    new_handler = NewHandler()
    # ancestor_handler = AncestorHandler()
    bus.subscribe(RootCommand, root_handler)
    bus.subscribe(NewCommand, new_handler)
    # bus.subscribe(AncestorCommand, ancestor_handler)

    # Read json-object-like commands from the input file
    commands = read_data('tests', 'initmode', 'init.in')
    open_command = commands.pop(0)
	
    # Check connection with the specified database
    try:
        with psycopg2.connect(host='localhost', 
                        dbname=open_command['open']['database'],
                        user=open_command['open']['user'],
                        password=open_command['open']['password']) \
                    as db_conn:
        
            print(json.JSONEncoder().encode({'status': 'OK'}))

            # init database
            mode = init_db(db_conn, 'init', 'init.sql')

    # Connection error
    except psycopg2.DatabaseError:
        print(json.JSONEncoder().encode({'status': 'ERROR'}))
        commands = []   # delete all commands

    # invoke each command
    for command in commands:
        with psycopg2.connect(host='localhost', 
                        dbname=open_command['open']['database'],
                        user=open_command['open']['user'],
                        password=open_command['open']['password']) \
                    as db_conn:

            if 'root' in command:
                # root only in init mode
                root = RootCommand(db_conn, command['root'], mode)
                bus.publish(root)

            if  'new' in command:
                new = NewCommand(db_conn, command['new'])
                bus.publish(new)
                

if __name__ == "__main__":
    main()
