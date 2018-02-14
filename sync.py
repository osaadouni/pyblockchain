from block import Block
from chain import Chain
from config import *
from utils import is_valid_chain

import os
import json
import requests
import glob
import sys

def sync_local():
    local_chain = Chain([])

    #We're assuming that the folder and at least initial block exists 
    if os.path.exists(CHAINDATA_DIR):
        for filepath in sorted(glob.glob(os.path.join(CHAINDATA_DIR, '*.json'))):
            with open(filepath, 'r') as block_file:
                try:
                    block_info = json.load(block_file)
                except:
                    print filepath

                print 'block_info:'
                print block_info

                local_block = Block(block_info)
                local_chain.add_block(local_block)

    return local_chain


def sync_overall(save=False):

    best_chain = sync_local()

    print 'sync_local():'
    print best_chain

    print best_chain.block_list_dict()
    #sys.exit(0)

    for peer in PEERS:

        #try to connect to peer
        peer_blockchain_url = peer + 'blockchain.json'
            
        print 'peer_blockchain_url: ', peer_blockchain_url 

        try:
            r = requests.get(peer_blockchain_url)
                
            peer_blockchain_dict = r.json()
                
            print 'peer_blockchain_dict: ', peer_blockchain_dict 

            peer_blocks = [Block(bdict) for bdict in peer_blockchain_dict]
            peer_chain = Chain(peer_blocks)

            if peer_chain.is_valid() and peer_chain > best_chain:
                best_chain = peer_chain 

        except requests.exceptions.ConnectionError:
            print "Peer at %s not running. Continuing to next peer." % peer

    print "Longest blockchain is %s blocks" % len(best_chain)

    # for now, save the new blockchain over whatever was there
    if save:
        best_chain.self_save()

    return best_chain


def sync(save=False):

    return sync_overall(save=save)


if __name__ == '__main__':
    node_blocks = sync()
    print node_blocks

    for b in node_blocks:
        print b.__dict__()
