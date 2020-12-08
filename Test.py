import pygame, sys, random
import numpy as np
from collections import deque
from GameConstants import GameConstants
from Environment import Environment
from keras.models import load_model
# from DQN import DQN

pygame.init()
screen = pygame.display.set_mode(GameConstants.SCREEN_SIZE)
pygame.display.set_caption('Navigation')

clock = pygame.time.Clock()

env = Environment(screen=screen)


list_ep_rewards_test = []
penalty, prize = 0,0
reward = 0

# load model
main_model = load_model('model-0.10.h5')
f = open('data_test.text', 'a')
for episode in range(GameConstants.NUM_EPISODES_TEST):

    curr_state = env.reset(episode, level=8,test = True)
    done = False
    episode_reward, episode_step = 0, 0
    epsilon = 1. / ((episode / 10) + 1)
    nodes_robot = []
    nodes_goal = []
    while not done:
        # clock.tick(200)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        pygame.draw.rect(screen, (255, 0, 0), env.robot, 0)
        
        for i in range(10):
                pygame.draw.rect(screen, (135,206,250), env.obs_rects[i], 0)
        for i in range(10,12):
            #Moving
            pygame.draw.rect(screen, (255, 215, 0), env.obs_rects[i], 0)
            
        pygame.draw.rect(screen, (255,20,147), env.obs_rects[12], 0)
        
        
        pygame.draw.rect(screen, (0, 255, 0), env.goal, 0)
        
        if episode_step == 0:
            pygame.image.save(screen, f'first_state-{episode}.jpg')
            
        nodes_robot.append((env.robot.x,env.robot.y))
        nodes_goal.append((env.goal.x,env.goal.y))

        action = np.argmax(main_model.predict(curr_state.reshape(-1, *curr_state.shape)))

        next_state, reward, done = env.step(action, test=True)

        episode_reward += reward
        episode_step += 1
        curr_state = next_state

        pygame.display.update()

    list_ep_rewards_test.append(episode_reward)
    avg_ep_reward_test = np.mean(list_ep_rewards_test)
    print(f'episode:{episode}, reward:{episode_reward:.2f}, steps:{episode_step}',end='')
    f.write(f'episode: {episode}, reward: {episode_reward:.2f}, steps: {episode_step}')

    if reward == GameConstants.OBSTACLE_PENALTY:
        print(', -obstacle collision-')
        f.write(', -obstacle collision-\n')
        penalty += 1
    elif reward == GameConstants.GOAL_REWARD:
        print(', -goal found-')
        f.write(', -goal found-\n')
        prize += 1
        # main_model.save(f'epreward/{episode_reward}_steps/{steps} .model')
    else:
        print()
        f.write('\n')

    if (episode + 1) % GameConstants.EPISODE_REPORT_COUNT == 0:
        print('\nResults up till now')
        print('obstacle collision: ', penalty)
        print('goal found: ', prize)
        print('max step: ', episode - penalty - prize)
        print('mean reward: ', np.mean(list_ep_rewards_test))
        f.write(f'\nResults up till now\nobstacle collision: {penalty}\ngoal found: {prize}\nmax step: {episode - penalty - prize}\nmean reward: {np.mean(list_ep_rewards_test[-GameConstants.EPISODE_REPORT_COUNT:])}\n\n')

    for i in range(len(nodes_robot)-1):
        pygame.draw.circle(screen, (188,143,143), nodes_robot[i], 4)
        
    pygame.image.save(screen, f'final_state-{episode}-{env.a}.jpg')
        
    for i in range(len(nodes_robot)-1):
        pygame.draw.circle(screen, (188,143,143), nodes_goal[i], 4)
        

    
    #pygame.image.save(screen, f'final_state-{episode}-{env.a}-goal.jpg')