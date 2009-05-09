
class Dungeon(object):
    def __init__(self, height, width):        
        self.map  = {}
        self.height = height
        self.width = width
        
    def __getitem__(self,key):
        index = key[0] + key[1] * self.width
        if (self.map.has_key(index)):
            return self.map[index]
        else:
            reurn None

    def __setitem__(self,key,value):
        index = key[0] + key[1] * self.width
        self.map[index] = value;
            

        
        
        
    
