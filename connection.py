#!/usr/bin/env python

class Connection(object):
    def __init__(self, a, b):
        assert(a != b)
        if ( b > a ):
            self.value = (a, b)
        else:
            self.value = (b, a)
    
    def __eq__(self,other):
        return ( other.value == self.value )
    
    def __str__(self):
        return "Connecting (%d,%d) " % (self.value[0], self.value[1])
    
    def __hash__(self):
        return self.value.__hash__()
        
    def __len__(self):
        return 2
    
    def __getitem__(self,key):
        assert(key >= 0)
        assert(key < 2)
        return self.value[key]
        
    def __contains__(self,item):
        return (item in self.value)

    def other(self,i):
        if ( i == self.value[0] ):
            return self.value[1]
        else:
            return self.value[0]
        
        
