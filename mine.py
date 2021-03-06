from block import Block
import datetime as date
import time
import sync
import json
import hashlib
import sys

import apscheduler 
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# If we're running mine.py, we don't want it in the background 
# because the script would return after starting. So we want the 
# BlockingScheduler to run the code.

sched = BlockingScheduler(standalone=True)

NUM_ZEROS = 5 

STANDARD_ROUNDS = 100000

def mine_for_block(chain=None, rounds=STANDARD_ROUNDS, start_nonce=0):
    if not chain:
        chain = sync.sync_local() # gather last node 

    prev_block = chain.most_recent_block()

    return mine_from_prev_block(prev_block, rounds=rounds, start_nonce=start_nonce)


def mine_from_prev_block(prev_block, rounds=STANDARD_ROUNDS, start_nonce=0):
    # create new block with correct nonce
    new_block = utils.create_new_block_from_prev(prev_block=prev_block)
    return mine_block(new_block, rounds=rounds, start_nonce=start_nonce)



def mine_block(new_block, rounds=STANDARD_ROUNDS, start_nonce=0):
    # Attempting to find a vlid nonce to match the required difficulty 
    # of leading zeros. We're only going to try 1000
    nonce_range = [i+start_once for i in range(rounds)]

    for nonce in nonce_range:
        new_block.nonce = nonce 
        new_block.update_self_hash()
        if str(new_block.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            print 'block %s mined. Nonce: %s' % (new_block.index, new_block.nonce)
            assert new_block.is_valid()
            return new_block, rounds, start_nonce
    
    # couldn't find a hash to work with, return rounds and start_nonce
    # as well so we can know what we tried
    return None, rounds, start_nonce

def generate_header(index, prev_hash, data, timestamp, nonce):
    return str(index) + prev_hash + data + str(timestamp) + str(nonce)

def calculate_hash(index, prev_hash, data, timestamp, nonce):
    header_string = generate_header(index, prev_hash, data, timestamp, nonce)

    print '\n'
    print 'header_string: %s' % header_string 
    sha = hashlib.sha256()
    sha.update(header_string)
    return sha.hexdigest()


def mine(last_block):

    index = int(last_block.index) + 1 
    timestamp = date.datetime.now()
    data = "I block #%s" % (int(last_block.index) + 1 ) # random string for now, not transactions
    prev_hash = last_block.hash
    nonce = 0 

    block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

    print 'nonce: %s'  % nonce
    print 'block_hash: %s'  % block_hash
    while str(block_hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        
        nonce += 1 
        block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
        print 'nonce: %s'  % nonce
        print 'block_hash: %s'  % block_hash

    # dictionary to create the new block object
    block_data = {}
    block_data['index'] = index
    block_data['prev_hash'] = last_block.hash
    block_data['timestamp'] = timestamp
    block_data['data'] = "Gimme some %s dollars" % index
    block_data['hash'] = block_hash
    block_data['nonce'] = nonce

    return Block(block_data)


if __name__ == '__main__':
    node_blocks = sync.sync() # gather last node 

    print 'node_blocks: ' 
    print node_blocks 

    prev_block = node_blocks[-1]
    print prev_block.__dict__()
    #sys.exit()
    new_block = mine(prev_block)
    new_block.self_save()

    print new_block
