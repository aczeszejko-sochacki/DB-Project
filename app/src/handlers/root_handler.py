from commandbus import Command, CommandHandler
import json

class RootHandler(CommandHandler):
    """Handle root command"""

    def handle(self, RootCommand: Command):

        # Root command only available in init mode
        if RootCommand.mode == 'init':
            with RootCommand.db_conn.cursor() as cur:
                
                # Root has not a supervisor
                if RootCommand.params['secret'] != 'qwerty':
                    print(json.JSONEncoder().encode({'status': 'ERROR'}))

                # Transaction
                cur.callproc('root', (
                        RootCommand.params['emp'],
                        RootCommand.params['newpassword'],
                        RootCommand.params['data']))

                RootCommand.db_conn.commit()

                print(json.JSONEncoder().encode({'status': 'OK'}))

        else:
            # Transaction failed
            print(json.JSONEncoder().encode({'status': 'ERROR'}))
