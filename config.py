CHAINDATA_DIR = 'chaindata/'

BROADCASTED_BLOCK_DIR = CHAINDATA_DIR + 'bblocks/'

NUM_ZEROS = 5 # difficulty, currently

BLOCK_VAR_CONVERSIONS = {'index': int, 'nonce': int, 'hash': str, 'prev_hash': str, 'timestamp': int}


#possible peers to start with 
PEERS = [

            'http://localhost:5000/', 
            'http://localhost:5001/', 
            'http://localhost:5002/', 
            'http://localhost:5003/', 
        ]




