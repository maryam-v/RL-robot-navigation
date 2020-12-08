from math import sqrt


class vector(object):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def cal_vector(self,p1,p2):
        self.x = p2[0]-p1[0]
        self.y = p2[1]-p1[1]
        return (self.x,self.y)
    def get_magnitude(self):
        return sqrt(self.x**2+self.y**2)
