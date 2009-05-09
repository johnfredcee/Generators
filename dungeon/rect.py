
class Rect(object):
    
    def __init__(self, x0, y0, x1, y1):
        if (x0 > x1):
            t = x0
            x0 = x1
            x1 = t
        if (y0 > y1):
            t = y0
            y0 = y1
            y1 = t    
        self.value = (x0, y0, x1, y1)

    def __getitem__(self, key):
        return self.value[key]

    def __len__(self):
        return 4

    def __eq__(self,other):
        return ( other.value == self.value )

    def inside(self, point):
        return ((point[0] >= self.value[0]) and (point[0] <= self.value[2]) and (point[1] >= self.value[1]) and (point[1] <= self.value[3]))
                
        
    def intersects(self, other):
        # is a point
        if (len(other) == 2):
            return self.inside(other)
        # is another rect
        if (len(other) == 4):
            return (not((other[2] < self.value[0]) and (other[0] > self.value[2]) and (other[3] < self.value[1]) and (other[1] > self.value[3])))
                        



