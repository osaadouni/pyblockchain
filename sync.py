from block import Block

import os
import json

def sync():
    node_blocks = []
    
    #we're assuming that the folder and at least initial block exists
    chaindata_dir = 'chaindata'

    if os.path.exists(chaindata_dir):
        for filename in sorted(os.listdir(chaindata_dir)):
            if filename.endswith('.json'):  # DS_Store sometimes screws things up
                filepath = '%s/%s' % (chaindata_dir, filename)
                with open(filepath, 'r') as block_file:
                        
                    print 'block_file => %s' % block_file 

                    block_info = json.load(block_file)
                    block_object = Block(block_info)
                    node_blocks.append(block_object)

    return node_blocks



if __name__ == '__main__':
    node_blocks = sync()
    print node_blocks

    for b in node_blocks:
        print b.__dict__()
