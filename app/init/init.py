import sys
import os
import psycopg2

def init_db(db):
    """
    Init tables, funtions etc. needed
    to maintain data
    """
   
    try:
        mode = sys.argv[1]      # --init mode

        if mode == '--init':
            with open (file=os.path.join('init', 'init.sql')) \
                        as init_data:
                cur = db.cursor()
                print('Creating database...')
                cur.execute(init_data.read())
                print('...done')
                cur.close()

    except IndexError:
        pass        # normal mode



