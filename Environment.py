import pygame, random
import numpy as np
from GameConstants import GameConstants
from Obstacles import Obstacles
from Lidar import Lidar


class Environment:
    def __init__(self, screen):
        self.moving_obs = 0
        self.movespeed = 1
        self.dyenv = 0
        self.obstacle_flag = 0
        self.higher_x = GameConstants.SCREEN_SIZE[0] - GameConstants.ROBOT_SIZE[0]
        self.higher_y = GameConstants.SCREEN_SIZE[1] - GameConstants.ROBOT_SIZE[1]
        self.screen = screen
        self.lidar_A = Lidar([0,0],self.screen)
        
        
        self.direction = [1,0]
        self.coeff_reward = 1
        self.x=0
        
        
        self.movespeed_goal = 1
        self.dyenvgoal = 0
        self.goal_flag = 0


    def lidarState(self):
        state = self.lidar_A.state_2()
        if len(state) < 400:
            for i in range(20):
                state.append([self.goal.x - self.robot.x, self.goal.y - self.robot.y])  # car_A.positon()是一个tuple，需要拆分
            for i in range(20):
                state.append([self.goal.x - self.robot.x, self.goal.y - self.robot.y])
        else:
            for i in range(20):
                state[360 + i] = [self.goal.x - self.robot.x, self.goal.y - self.robot.y]
            for i in range(20):
                state[380 + i] = [self.goal.x - self.robot.x, self.goal.y - self.robot.y]
        return state

    def processState(self, state):
        return np.reshape(state,[800])

    def reset(self,episode_num, level = 0,test = False):
        self.a = random.randint(0,4)
        if self.a==0 or self.a==1 or self.a==2 or self.a==3:
            self.maxgoal=100
        elif self.a==4:
            self.maxgoal=50
        self.episode_step = 0
        self.level = level

        self.obstacle = Obstacles(level=self.level)
        self.obs_rects=self.obstacle.rectObs


        x = random.randint(0, GameConstants.SCREEN_SIZE[0] - GameConstants.GOAL_SIZE[0])
        y = random.randint(0, GameConstants.SCREEN_SIZE[1] - GameConstants.GOAL_SIZE[1])
        self.goal = pygame.Rect((x, y), GameConstants.GOAL_SIZE)


        while self.goal.collidelist(self.obs_rects)!=-1:
            x = random.randint(0, GameConstants.SCREEN_SIZE[0] - GameConstants.GOAL_SIZE[0])
            y = random.randint(0, GameConstants.SCREEN_SIZE[1] - GameConstants.GOAL_SIZE[1])
            self.goal = pygame.Rect((x, y), GameConstants.GOAL_SIZE)



        x = random.randint(0, GameConstants.SCREEN_SIZE[0] - GameConstants.ROBOT_SIZE[0])
        y = random.randint(0, GameConstants.SCREEN_SIZE[1] - GameConstants.ROBOT_SIZE[1])
        self.robot = pygame.Rect((x, y), GameConstants.ROBOT_SIZE)

        while self.robot.collidelist(self.obs_rects) != -1 or self.robot.colliderect(self.goal):
            x = random.randint(0, GameConstants.SCREEN_SIZE[0] - GameConstants.ROBOT_SIZE[0])
            y = random.randint(0, GameConstants.SCREEN_SIZE[1] - GameConstants.ROBOT_SIZE[1])
            self.robot = pygame.Rect((x, y), GameConstants.ROBOT_SIZE)


        self.lidar_A.pos_change([self.robot.x, self.robot.y])
        self.lidar_A.scan()
        s =self.lidarState()
        observation = self.processState(s)
        observation = np.reshape(observation, [20,20,2])


        return observation


    def move_direction(self, choice, speed = GameConstants.SPEED):       
        if choice == 0:
            self.direction = [1, 0]
        if choice == 1:
            self.direction = [1, 1]
        if choice == 2:
            self.direction = [0, 1]
        if choice == 3:
            self.direction = [-1, 1]
        if choice == 4:
            self.direction = [-1, 0]
        if choice == 5:
            self.direction = [-1, -1]
        if choice == 6:
            self.direction = [0, -1]
        if choice == 7:
            self.direction = [1, -1]
        

        if abs(choice-self.x)==0:
            self.coeff_reward = 1
        elif abs(choice-self.x)==1 or abs(choice-self.x)==7:
            self.coeff_reward = 2        
        elif abs(choice-self.x)==2 or abs(choice-self.x)==6:
            self.coeff_reward = 3
        elif abs(choice-self.x)==3 or abs(choice-self.x)==5:  
            self.coeff_reward = 4
        elif abs(choice-self.x) == 4:
            self.coeff_reward = 5
            
            
        self.x=choice
            
        final_direction = [self.direction[0]*speed, self.direction[1]*speed]

        return final_direction
    

    
    
    def update_moving_goal(self):
        if (self.dyenvgoal >= self.maxgoal and self.goal_flag == 0):
            self.goal_flag = 1
        elif (self.goal_flag == 1 and self.dyenvgoal > 0):
            self.movespeed_goal = -1
        else:
            self.goal_flag = 0
            self.movespeed_goal = 1
        self.dyenvgoal += self.movespeed_goal

           

        if self.a==0:
            self.goal.move_ip(0, self.movespeed_goal)
        elif self.a==1:
            self.goal.move_ip(self.movespeed_goal, 0)
        elif self.a==2:
            self.goal.move_ip(self.movespeed_goal, self.movespeed_goal)
        elif self.a==3:
            self.goal.move_ip(-self.movespeed_goal, self.movespeed_goal)
        else:
            self.goal.move_ip(-self.movespeed_goal**4, -self.movespeed_goal)
            
    
    def step(self,action,test=False):
        done_step = False
        reward_step = 0
        self.episode_step +=1
        if self.level == 3 or self.level == 4 or self.level == 5 or self.level==6 or self.level==8:
            self.obs_rects = self.obstacle.update_moving_obs()
        if not test:
            (dirX,dirY) = self.move_direction(action)
        else:
            (dirX, dirY) = self.move_direction(action, speed= GameConstants.SPEED_TEST)
        # print(dirX,dirY)

        self.robot.move_ip(dirX, dirY)
        
        self.update_moving_goal()


        if self.robot.colliderect(self.goal):
            reward_step = GameConstants.GOAL_REWARD
            done_step = True
        if self.robot.collidelist(self.obs_rects)!=-1:
            reward_step = GameConstants.OBSTACLE_PENALTY
            done_step = True
        if self.episode_step >= GameConstants.MAX_EPISODE_STEP:
            done_step = True

        if not done_step:
            reward_step = GameConstants.STEP_PENALTY*self.coeff_reward

        if self.robot.x > GameConstants.SCREEN_SIZE[0] - GameConstants.ROBOT_SIZE[0]:
            self.robot.x = GameConstants.SCREEN_SIZE[0] - GameConstants.ROBOT_SIZE[0]

        if self.robot.y > GameConstants.SCREEN_SIZE[1] - GameConstants.ROBOT_SIZE[1]:
            self.robot.y = GameConstants.SCREEN_SIZE[1] - GameConstants.ROBOT_SIZE[1]

        if self.robot.x <= 0:
            self.robot.x = 0

        if self.robot.y <= 0:
            self.robot.y = 0

            
            
        ## Goal colliding boundaries    
        if self.goal.x > GameConstants.SCREEN_SIZE[0] - GameConstants.GOAL_SIZE[0]:
            self.goal.x = GameConstants.SCREEN_SIZE[0] - GameConstants.GOAL_SIZE[0]
            
        if self.goal.y > GameConstants.SCREEN_SIZE[1] - GameConstants.GOAL_SIZE[1]:
            self.goal.y = GameConstants.SCREEN_SIZE[1] - GameConstants.GOAL_SIZE[1]
            
        if self.goal.x <= 0:
            self.goal.x = 0
            
        if self.goal.y <= 0:
            self.goal.y = 0



        self.lidar_A.pos_change([self.robot.x, self.robot.y])
        self.lidar_A.scan()
        s =self.lidarState()
        new_observation = self.processState(s)
        new_observation = np.reshape(new_observation, [20,20,2])


        return new_observation, reward_step, done_step