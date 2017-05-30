import hashlib
import struct

class HashTable:
    
    def __init__(self, buckets):
        self.table = [None]*buckets
        self.buckets = buckets
        self.counter = 0
        
    def hash_function(self, value):
        h = hashlib.md5() # instantiate hash function
        h.update(bytes(value)) # hash the value
        num = struct.unpack(">L", h.digest()[0:4])[0] # unpack bytestring to number
        return num
       
    def hash_table_increase(self):
        carrier = self.table[:]
        self.buckets = self.buckets * 2
        self.table = [None]*self.buckets
        self.counter = 0
        
        for i in carrier:
            self.insert(i)

    
    #Search from current position for empty spots and matching values    
    def traverse(self, value, index, on_find, on_empty):
        
        for i in range(index, index + self.buckets): 
            index = index + i % self.buckets

            if self.table[index] == value:
                return on_find(self, value, index)

            elif not self.table[index]:
                return on_empty(self, value, index)
    
    
    def insert(self, value):
        index = self.hash_function(value) % self.buckets
        #print "inserting {0} into slot {3}, counter = {1}, buckets = {2}".format(value, self.counter, self.buckets,
        #                                                                        index)
        if not self.table[index]:
            self.table[index] = value
            self.counter +=1
            
        elif self.table[index] and self.counter < self.buckets and self.table[index] != value: 
            def empty_insert(self, value, index):
                self.table[index] = value
                self.counter +=1
                
            noop = lambda self,value,index: None
            self.traverse(value, index, on_find=noop, on_empty=empty_insert)
                    
        elif self.counter == self.buckets:
            self.hash_table_increase()
            self.insert(value)

        
    #given an element see if it is contained in the hash table
    def __contains__(self, item):
        
        index = self.hash_function(item) % self.buckets
        
        if self.table[index] == item:
            return True
        
        elif not self.table[index]:
            return False
        else:
            on_find = lambda self,value,index: True
            on_empty = lambda self,value,index: False
            return self.traverse(item, index, on_find=on_find, on_empty=on_empty)

        return False
        
    def __repr__(self):
        return str(self.table)
    
        
class DoubleHashTable(HashTable):
    
    def hash_function(self,value):
        h = hashlib.md5() # instantiate hash function
        h.update(bytes(value)) # hash the value
        num = struct.unpack(">L", h.digest()[0:4])[0] # unpack bytestring to number
        return num
    
    def hash_function_traversal(self, value):
        h = hashlib.sha256() # instantiate hash function
        h.update(bytes(value)) # hash the value
        num = struct.unpack(">L", h.digest()[0:4])[0] # unpack bytestring to number
        return num
    
    def traverse(self, value, index, on_find, on_empty):
        for i in range(index, index + self.buckets): 
            
            index = index + i*self.hash_function_traversal(value) % self.buckets

            if self.table[index] == value:
                return on_find(self, value, index)

            elif not self.table[index]:
                return on_empty(self, value, index)