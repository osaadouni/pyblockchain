import hashlib
import os
import json
import datetime as date 
from config import *

class Block(object):

    def __init__(self, dictionary):
        '''
            We're looking for index, timestamp, data, prev_hash, nonce
        '''
        for key, value in dictionary.items():
            if key in BLOCK_VAR_CONVERSIONS:    
                
                print key , BLOCK_VAR_CONVERSIONS[key]

                setattr(self, key, BLOCK_VAR_CONVERSIONS[key](value))
            else:
                setattr(self, key, value)
        
        if not hasattr(self, 'nonce'):
            self.nonce = 'None'
                
        if not hasattr(self, 'hash'): # in creating the first block, needs to be remove in future
            self.hash = self.update_self_hash()

    def header_string(self):

        return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)

    def generate_header(index, prev_hash, data, timestamp, nonce):

        return str(index) + prev_hash + data + str(timestamp) + str(nonce)


    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string())
        new_hash = sha.hexdigest()
        self.hash = new_hash
        return new_hash

    def self_save(self):

        # check if the chaindata folder exists 
        if not os.path.exists(CHAINDATA_DIR):
            #make chaindata dir 
            os.mkdir(CHAINDATA_DIR)

        index_string = str(self.index).zfill(6) #left pad zeros, numerical order
        filename = '%s%s.json' % (CHAINDATA_DIR, index_string)
        print filename 
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)
             
    def to_dict(self):
        
        info = {}
        info['index']     = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash']      = str(self.hash)
        info['data']      = str(self.data)
        info['nonce']     = str(self.nonce)
        return info


    def is_valid(self):
        self.update_self_hash()
        if str(self.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            return True
        else:
            return False


    def __repr__(self):
        
        return "Block<index: %s>, <hash: %s>" % (self.index, self.hash)


    def __eq__(self, other):
        
        return (self.index == other.index and
            self.timestamp == other.timestamp and 
            self.prev_hash == other.prev_hash and 
            self.hash == other.hash and
            self.data == other.data and
            self.nonce == other.nonce)

    def __ne__(self, other):
        
        return not self.__eq__(other)

    def __gt__(self, other):
        
        return self.timestamp < other.timestamp

    def __lt__(self, other):

        return self.timestamp > other.timestamp 


def create_first_block():
    # index zero and arbitrary previous hash 
    block_data = {}
    block_data['index']     = 0 
    block_data['timestamp'] = date.datetime.now()
    block_data['data']      = 'First block data'
    block_data['prev_hash'] = ''
    block_data['nonce']     = 0 # starting it at 0 
    block = Block(block_data)
    return block


if __name__ == '__main__':

    # check if the chaindata folder exists 
    if not os.path.exists(CHAINDATA_DIR):
        #make chaindata dir 
        os.mkdir(CHAINDATA_DIR)

    # check if dir is empty from just creation or from before
    if os.listdir(CHAINDATA_DIR) == []:

        print 'create genesis block ...'
        #create and save first block/genesis block
        first_block = create_first_block()
        print(first_block.to_dict())

        first_block.self_save()
    else:
        print '%s not empty' % (CHAINDATA_DIR)
