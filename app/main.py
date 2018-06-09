import psycopg2
from commandbus import Command, CommandHandler, CommandBus
from src import read_data
from init import init_db
from src import RootCommand
from src import NewCommand
from src import AncestorCommand
from src import RootHandler
from src import NewHandler
from src import AncestorHandler

if __name__ == "__main__":
    """
    Main. Init database, create command bus, 
    receive commands and pass to handlers
    """

    # init commandbus and handlers
    bus = CommandBus()
    root_handler = RootHandler()
    new_handler = NewHandler()
    ancestor_handler = AncestorHandler()
    bus.subscribe(RootCommand, root_handler)
    bus.subscribe(NewCommand, new_handler)
    bus.subscribe(AncestorCommand, ancestor_handler)

    # read json-object-like commands from the input file
    commands = read_data('tests', 'initmode', 'init.in')
    open_command = commands.pop(0)
	
    # open connection with the specified database
    with psycopg2.connect(host='localhost', 
                        dbname=open_command['open']['database'],
                        user=open_command['open']['login'],
                        password=open_command['open']['password']) \
                    as db_conn:

        mode = init_db(db_conn)
        
        # invoke each command
        for command in commands:
            if 'root' in command:
                # root only in init mode
                root = RootCommand(db_conn, command['root'], mode)
                bus.publish(root)

            if  'new' in command:
                new = NewCommand(db_conn, command['new'])
                bus.publish(new)
            
            if 'ancestor' in command:
                # ancestor only in normal mode
                ancestor = AncestorCommand(db_conn, command['ancestor'], mode)
                bus.publish(ancestor)

