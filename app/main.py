import psycopg2
import json
import sys
from commandbus import Command, CommandHandler, CommandBus
from init import init_db
from src import *

def main():
    """
    Main. Init database, create command bus, 
    receive commands and pass to handlers
    """

    # Init commandbus
    bus = CommandBus()

    # Init handlers for commands
    root_handler = RootHandler()
    new_handler = NewHandler()
    parent_handler = ParentHandler()
    child_handler = ChildHandler()
    read_handler = ReadHandler()
    update_handler = UpdateHandler()
    ancestor_handler = AncestorHandler()
    ancestors_handler = AncestorsHandler()
    descendants_handler = DescendantsHandler()
    remove_handler = RemoveHandler()
    open_handler = OpenHandler()

    # Route commands to coresponding handlers
    bus.subscribe(RootCommand, root_handler)
    bus.subscribe(NewCommand, new_handler)
    bus.subscribe(ParentCommand, parent_handler)
    bus.subscribe(ChildCommand, child_handler)
    bus.subscribe(ReadCommand, read_handler)
    bus.subscribe(UpdateCommand, update_handler)
    bus.subscribe(AncestorCommand, ancestor_handler)
    bus.subscribe(AncestorsCommand, ancestors_handler)
    bus.subscribe(DescendantsCommand, descendants_handler)
    bus.subscribe(RemoveCommand, remove_handler)
    bus.subscribe(OpenCommand, open_handler)

    # Get transaction mode
    mode = 'normal'
    try:
        mode = sys.argv[1][2:]
    except IndexError:
        pass


    # Read json-object-like commands from the input file
    commands = read_data(input())
    open_command = commands.pop(0)
	
    # Check connection with the specified database
    bus.publish(OpenCommand(open_command))

    # init database
    init_db(open_command, 'init', 'init.sql')

    # invoke each command
    for command in commands:
        with psycopg2.connect(host='localhost', 
                        dbname=open_command['open']['database'],
                        user=open_command['open']['user'],
                        password=open_command['open']['password']) \
                    as db_conn:

            try:
                command_name = globals()[
                        list(command.keys())[0].title() + 'Command']

                command_instance = command_name(db_conn, 
                                    list(command.values())[0], mode)

                # Handle command
                bus.publish(command_instance)

            except KeyError:
                # Command key should be valid
                print(json.JSONEncoder().encode({'status': 'ERROR'}))
               

if __name__ == "__main__":
    main()
