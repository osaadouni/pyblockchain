import hashlib
import os
import json
import datetime as date 

class Block(object):

    def __init__(self, dictionary):
        '''
            We're looking for index, timestamp, data, prev_hash, nonce
        '''
        for k, v in dictionary.items():
            setattr(self, k, v)
        
        if not hasattr(self, 'nonce'):
            self.nonce = ''
                
        if not hasattr(self, 'hash'): # in creating the first block, needs to be remove in future
            self.hash = self.create_self_hash()

    def header_string(self):
        return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)
   
    def create_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string())
        return sha.hexdigest()

    def self_save(self):
        chaindata_dir = 'chaindata'
        index_string = str(self.index).zfill(6) #left pad zeros, numerical order
        filename = '%s/%s.json' % (chaindata_dir, index_string)
        print filename 
        with open(filename, 'w') as block_file:
            json.dump(self.__dict__(), block_file)
             
    def __dict__(self):
        
        info = {}
        info['index']     = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash']      = str(self.hash)
        info['data']      = str(self.data)
        info['nonce']      = str(self.nonce)
        return info

    def __str__(self):
        
        return "Block<prev_hash: %s,hash: %s>" % (self.prev_hash, self.hash)



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
    chaindata_dir = 'chaindata/'
    if not os.path.exists(chaindata_dir):
        #make chaindata dir 
        os.mkdir(chaindata_dir)

    # check if dir is empty from just creation or from before
    if os.listdir(chaindata_dir) == []:

        print 'create genesis block ...'
        #create and save first block/genesis block
        first_block = create_first_block()
        print(first_block.__dict__())

        first_block.self_save()
    else:
        print 'not empty'
