import sys
import os
import psycopg2

def init_db(open_command, *path):
    """
    Init tables, funtions etc. needed
    to maintain data
    """

    # Before init need to connect with the database
    db_params = list(open_command.values())[0]
   
    try:
        # Check if init mode enabled
        mode = sys.argv[1]

        if mode == '--init':
            try:
                with open(file=os.path.join(*path)) as init_data:
                    with psycopg2.connect(host='localhost',
                                        dbname=db_params['database'],
                                        user=db_params['user'],
                                        password=db_params['password']) \
                                    as db_conn:

                        with db_conn.cursor() as cur:
                            sql_code = init_data.read()
                            cur.execute(sql_code)

            except FileNotFoundError:
                print('Incorrect path to init.sql file')
                # Stop execution
                sys.exit(1)
            
    except IndexError:
        # Normal mode, no need to init
        pass

