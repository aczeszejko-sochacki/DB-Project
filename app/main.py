import psycopg2
import json
from commandbus import Command, CommandHandler, CommandBus
from init import init_db
from src import *

def main():
    """
    Main. Init database, create command bus, 
    receive commands and pass to handlers
    """

    # Init commandbus and handlers
    bus = CommandBus()
    root_handler = RootHandler()
    new_handler = NewHandler()
    parent_handler = ParentHandler()
    child_handler = ChildHandler()
    # ancestor_handler = AncestorHandler()
    bus.subscribe(RootCommand, root_handler)
    bus.subscribe(NewCommand, new_handler)
    bus.subscribe(ParentCommand, parent_handler)
    bus.subscribe(ChildCommand, child_handler)
    # bus.subscribe(AncestorCommand, ancestor_handler)

    # Read json-object-like commands from the input file
    commands = read_data(input())
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
    except psycopg2.DatabaseError as error:
        print(error)
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
                # new in both modes
                new = NewCommand(db_conn, command['new'])
                bus.publish(new)

            if 'parent' in command:
                # parent only in normal mode
                parent = ParentCommand(db_conn, command['parent'], mode)
                bus.publish(parent)

            if 'child' in command:
                # child only in normal mode
                child = ChildCommand(db_conn, command['child'], mode)
                bus.publish(child)
                

if __name__ == "__main__":
    main()
