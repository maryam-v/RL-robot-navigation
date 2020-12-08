from GameConstants import GameConstants
import pygame


class Obstacles:
    def __init__(self, level):
        self.movespeed = 1
        self.dyenv = 0
        self.obstacle_flag = 0
        self.rectObs = []
        self.level = level
        self.maxstep = 100
        if self.level == 0:
            self.rectObs.append(pygame.Rect((100, 50), GameConstants.OBSTACLE_SIZE))
        
        if self.level == 1:
            self.rectObs.append(pygame.Rect((50, 50), GameConstants.OBSTACLE_SIZE))
            self.rectObs.append(pygame.Rect((110, 120), GameConstants.OBSTACLE_SIZE))
        
        if self.level == 2:
            self.rectObs.append(pygame.Rect((50, 50), GameConstants.OBSTACLE_SIZE))

        if self.level == 3:
            self.rectObs.append(pygame.Rect((40,40),(40,40)))
            self.rectObs.append(pygame.Rect((140, 140), (80, 80)))
            self.rectObs.append(pygame.Rect((350, 400), (40, 40)))
            self.rectObs.append(pygame.Rect((500, 160), (40, 40)))
            self.rectObs.append(pygame.Rect((380, 100), (40, 40)))
            self.rectObs.append(pygame.Rect((300, 340), (80, 40)))
            self.rectObs.append(pygame.Rect((80 + self.dyenv, 300 ), (20, 20)))
            self.rectObs.append(pygame.Rect((280 + self.dyenv, 240), (20, 20)))
            self.rectObs.append(pygame.Rect((500, 300 + self.dyenv), (20, 20)))
            self.rectObs.append(pygame.Rect((400, 250 + self.dyenv), (20, 20)))

        if self.level == 4:
            self.rectObs.append(pygame.Rect((200, 80), (20, 200)))
            self.rectObs.append(pygame.Rect((220, 80), (200, 20)))
            self.rectObs.append(pygame.Rect((200, 350), (200, 20)))
            self.rectObs.append(pygame.Rect((400, 200), (60, 60)))
            self.rectObs.append(pygame.Rect((80, 100), (40, 40)))
            self.rectObs.append(pygame.Rect((80, 200 + self.dyenv), (20, 20)))
            self.rectObs.append(pygame.Rect((280 + self.dyenv, 200), (20, 20)))
            self.rectObs.append(pygame.Rect((500, 300 + self.dyenv), (20, 20)))


            
        if self.level == 5:
            self.rectObs.append(pygame.Rect((90,140),(20,120)))
            self.rectObs.append(pygame.Rect((220, 70), (60, 60)))
            self.rectObs.append(pygame.Rect((380, 50), (100, 40)))
            self.rectObs.append(pygame.Rect((290, 210), (60, 20)))
            self.rectObs.append(pygame.Rect((310, 230), (20, 120)))
            self.rectObs.append(pygame.Rect((260,400), (100, 30)))
            self.rectObs.append(pygame.Rect((0, 320), (100, 20)))
            self.rectObs.append(pygame.Rect((80, 390), (40, 40)))
            self.rectObs.append(pygame.Rect((520, 150), (60, 40))) 
            self.rectObs.append(pygame.Rect((540, 290), (40, 100))) 
            

        if self.level == 6:
            self.rectObs.append(pygame.Rect((320,370),(180,20)))
            self.rectObs.append(pygame.Rect((480, 210), (20, 160)))
            self.rectObs.append(pygame.Rect((140, 100), (30, 150)))
            self.rectObs.append(pygame.Rect((80, 160), (150, 30)))            
            self.rectObs.append(pygame.Rect((370, 60), (80, 80)))
            self.rectObs.append(pygame.Rect((100, 370), (100, 40)))
            self.rectObs.append(pygame.Rect((290, 60+self.dyenv), (20, 20)))
            self.rectObs.append(pygame.Rect((80+self.dyenv, 310+self.dyenv), (20, 20)))
            
            self.maxstep = 30
            

        if self.level == 7:
            self.rectObs.append(pygame.Rect((50, 50), GameConstants.OBSTACLE_MOVING_SIZE))
            self.rectObs.append(pygame.Rect((110, 120), GameConstants.OBSTACLE_MOVING_SIZE))
            
        if self.level == 8:
            self.rectObs.append(pygame.Rect((120,280),(20,200)))
            self.rectObs.append(pygame.Rect((100,100),(80,20)))
            self.rectObs.append(pygame.Rect((140,0),(20,120)))
            self.rectObs.append(pygame.Rect((140,300),(80,20)))
            self.rectObs.append(pygame.Rect((350,0),(20,100)))
            self.rectObs.append(pygame.Rect((350,400),(20,100)))
            self.rectObs.append(pygame.Rect((400,340),(100,20)))
            self.rectObs.append(pygame.Rect((450,200),(150,20)))
            self.rectObs.append(pygame.Rect((500,0),(20,140)))
            self.rectObs.append(pygame.Rect((550,350),(20,500)))

            # MOVING
            self.rectObs.append(pygame.Rect((220+self.dyenv, 150), (20, 20)))
            self.rectObs.append(pygame.Rect((300+ self.dyenv, 240 ), (20, 20)))
            self.rectObs.append(pygame.Rect((40+self.dyenv , 200+self.dyenv), (20, 20)))


            self.maxstep=50
            
        if self.level == 9:
            self.rectObs.append(pygame.Rect((140,0),(20,140)))
            self.rectObs.append(pygame.Rect((110, 140), (80, 20)))
            self.rectObs.append(pygame.Rect((0, 290), (400, 20)))
            self.rectObs.append(pygame.Rect((380, 310), (20, 60)))
#            
            self.rectObs.append(pygame.Rect((420, 0), (20, 140)))
            self.rectObs.append(pygame.Rect((380, 140), (60, 20)))
            self.rectObs.append(pygame.Rect((480, 220), (160, 20)))
            self.rectObs.append(pygame.Rect((200, 380), (30, 30)))
            
            self.rectObs.append(pygame.Rect((520, 360), (20, 40)))
            self.rectObs.append(pygame.Rect((520, 80), (30, 30)))
            self.rectObs.append(pygame.Rect((270, 70), (40, 20)))
            
            
    def update_moving_obs(self):
        if (self.dyenv >=self.maxstep and self.obstacle_flag == 0):
            self.obstacle_flag = 1
        elif (self.obstacle_flag == 1 and self.dyenv > 0):
            self.movespeed = -1
        else:
            self.obstacle_flag = 0
            self.movespeed = 1
        self.dyenv += self.movespeed
        if self.level == 2:
            self.rectObs[0].move_ip(self.movespeed, 0)
        if self.level == 3:
            self.rectObs[-1].move_ip(0, self.movespeed)
            self.rectObs[-2].move_ip(0, self.movespeed)
            self.rectObs[-3].move_ip(self.movespeed, 0)
            self.rectObs[-4].move_ip(self.movespeed, 0)
        if self.level == 4:
            self.rectObs[5].move_ip(0, self.movespeed)
            self.rectObs[6].move_ip(self.movespeed, 0)
            self.rectObs[7].move_ip(0, self.movespeed)
        if self.level == 6:
            self.rectObs[-2].move_ip(0, self.movespeed)
            self.rectObs[-1].move_ip(self.movespeed**4,-self.movespeed)
        if self.level == 7:
            self.rectObs[-1].move_ip(0, self.movespeed)
            self.rectObs[-2].move_ip(self.movespeed, 0)
        if self.level == 8:
            self.rectObs[-1].move_ip(self.movespeed**4, self.movespeed)
            self.rectObs[-2].move_ip(self.movespeed, 0)
            self.rectObs[-3].move_ip(0, self.movespeed)

            

            


        return self.rectObs
