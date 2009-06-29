#!/usr/bin/env python
import math

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

    def closest(self, point, points):
        """ Given a list of points that we index, return the closest connection end point to point """
        result = 0
        candidate = points[self.value[0]]
        length0 = math.sqrt( ( point.x - candidate.x ) * ( point.x - candidate.x ) + ( point.y - candidate.y )  * ( point.y - candidate.y ) )
        candidate = points[self.value[1]]        
        length1 = math.sqrt( ( point.x - candidate.x ) * ( point.x - candidate.x ) + ( point.y - candidate.y )  * ( point.y - candidate.y ) )
        if (length1 < length0):
            result = 1
        return result
                
