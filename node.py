from block import Block
from flask import Flask 
import sync

import os
import json 

node = Flask(__name__)

node_blocks = sync.sync() # initial blocks that are synced 

@node.route('/blockchain.json', methods=['GET'])

def blockchain():
    '''
    Shoots back the blockchain, which in our case, is a json list of hashes
    with the block information which is: 
    _ index
    _ timestamp
    _ data 
    _ hash
    _ prev_hash
    '''

    node_blocks = sync.sync() # update if they've changed 

    # Convert our blocks into dicionaries 
    # so we can send them as json objects later
    python_blocks = []

    for block in node_blocks:
        '''
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = { 
            "index": block.index,
            "timestamp": block.timestamp, 
            "data": block.data, 
            "hash": block.hash,
            "prev_hash": block.prev_hash
        }
        '''

        python_blocks.append(block.__dict__())
  
    json_blocks = json.dumps(python_blocks)
    return json_blocks 


if __name__ == '__main__':
    node.run()
