import os
from config import *
from mine import find_valid_nonce
from block import Block
import datetime


def create_first_block():
    # index zero and arbitrary previous hash 
    block_data = {}
    block_data['index']     = 0 
    block_data['timestamp'] = datetime.datetime.now()
    block_data['data']      = 'First block data'
    block_data['prev_hash'] = ''
    block_data['nonce']     = 0 # starting it at 0 
    return Block(block_data)


if __name__ == '__main__':

    # check if the chaindata folder exists 
    if not os.path.exists(CHAINDATA_DIR):
        #make chaindata dir 
        os.mkdir(CHAINDATA_DIR)
    else:
        print 'Chaindata dir already exists with blocks.\nIf you want to regenerate the blocks, delete /chaindata and rerun'

    # check if dir is empty from just creation or from before
    if os.listdir(CHAINDATA_DIR) == []:

        print 'create genesis block ...'
        #create and save first block/genesis block
        first_block = create_first_block()

        first_block = find_valid_nonce(first_block)

        print(first_block.to_dict())

        first_block.self_save()
    else:
        print '%s not empty' % (CHAINDATA_DIR)
