import json
import os

def read_data(*args):
    """
    Read json-encoded commands from input file and return
    list of json-decoded commands
    """

    filename = os.path.join(*args)
	
    with open(filename) as json_objects:
        encoded_data = json_objects.read().split('\n')[:-1]
        decoded_data = list(map(
                    lambda line: json.loads(line), encoded_data))
		
    return decoded_data
		
