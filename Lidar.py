from GameConstants import GameConstants
from math import cos, sin
from vector import vector


class Lidar:
    def __init__(self, p, screen, distance=200, angle=0):
        self.x = p[0]
        self.y = p[1]
        self.distance = distance
        self.angle = 0
        self.lidar = (0, 0) 
        self.data = []  
        self.data_2 = []  
        self.screen = screen


    def scan(self):
        dis = []
        for i in range(0, 360, 1):  
            for j in range(1, 40):
                x1 = int(self.x + self.distance * cos(i * 3.14 / 180) * j / 40)
                y1 = int(self.y + self.distance * sin(i * 3.14 / 180) * j / 40)

                if (x1 > 0 and x1 < GameConstants.SCREEN_SIZE[0] and y1 > 0 and y1 < GameConstants.SCREEN_SIZE[1]):
                    pix = self.screen.get_at((x1, y1))


                if (x1 <= 0 or x1 >= GameConstants.SCREEN_SIZE[0] or y1 <= 0 or y1 >= GameConstants.SCREEN_SIZE[1]):
                    break
                elif (pix[0] > 100 and pix[1] > 100 and pix[2] > 100):
                    break
                else:
                    dis = [x1, y1]
                    
            if len(self.data) < 360:
                self.data.append(dis)
            else:
                self.data[i] = dis

            if (self.x > 0 and self.x < GameConstants.SCREEN_SIZE[0] and self.y > 0 and self.y < GameConstants.SCREEN_SIZE[1]):
                vec = vector()
                if dis != []:
                    vec.cal_vector((self.x, self.y), self.data[i])
                    scan_dis = vec.get_magnitude()
                    if (len(self.data_2) < 360):
                        self.data_2.append(
                            [i, scan_dis]) 
                    else:
                        self.data_2[i] = [i, scan_dis]

                else:
                    break

    def show(self):
        for d in self.data:
            vect = vector()
            vect.cal_vector((self.x, self.y), d)
            if (vect.get_magnitude() < 190):
                self.screen.set_at(d, (255, 0, 0))
        return self.data

    def state(self):
        return self.data

    def state_2(self):
        return self.data_2

    def pos_change(self, pos):
        self.x = pos[0]
        self.y = pos[1]