import json
import os
import sys

def read_data(filename):
    """
    Read json-encoded commands from input file and return
    list of json-decoded commands
    """
    try:	
        with open(os.path.join('tests', filename), 'r') as json_objects:
            encoded_data = json_objects.read().split('\n')[:-1]
            decoded_data = list(map(
                        lambda line: json.loads(line), encoded_data))
		
        return decoded_data

    except FileNotFoundError:
        print('File does not exist in tests/ directory')
        # Stop execution
        sys.exit(1)
		
