import sys
import os
import psycopg2

def init_db(db, *path):
    """
    Init tables, funtions etc. needed
    to maintain data
    """
   
    try:
        mode = sys.argv[1]      # --init mode

        if mode == '--init':
            with open (file=os.path.join(*path)) as init_data:
                with db.cursor() as cur:
                    cur.execute(init_data.read())
            
            return 'init'
        else:
            return 'normal'
    except IndexError:
        return 'normal'     # normal mode

