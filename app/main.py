from src import read_data
from init import init_db
import psycopg2

if __name__ == "__main__":
    """
    Main. Init database, create command bus, 
    receive commands and pass to handlers
    """
	
    # read json-object-like commands from the input file
    commands = read_data()
    open_command = commands[0]
	
    # open connection with the specified database
    with psycopg2.connect(host='localhost', 
                        dbname=open_command['open']['database'],
                        user=open_command['open']['login'],
                        password=open_command['open']['password']) \
                    as db_conn:

        init_db(db_conn)
