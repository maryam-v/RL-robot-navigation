import pygame, sys, random, time
import numpy as np
from collections import deque
from GameConstants import GameConstants
from Environment import Environment
from DQN import DQN
import matplotlib.pyplot as plt
from DuelingDQN import DuelingDQN

pygame.init()
screen = pygame.display.set_mode(GameConstants.SCREEN_SIZE)
pygame.display.set_caption('Navigation')

clock = pygame.time.Clock()

env = Environment(screen= screen)
#game = DQN()
game = DuelingDQN()


list_ep_rewards = []
list_average_rewards = []
list_goal_reached = []
replay_buffer = deque(maxlen = GameConstants.REPLAY_MEMORY_SIZE)
penalty, prize = 0,0

f = open('data.text', 'a')
start_time = time.time()
start = start_time
epsilon = 1
DELAY_TRAINING = 1_000



for episode in range(GameConstants.NUM_EPISODES):
    if episode%5==0:
        level = random.choice([3,4,6,9])
    curr_state = env.reset(episode, level=level)
    done = False
    episode_reward, episode_step = 0, 0
    if epsilon <= 0.01:
        epsilon = 0.01
    else:
        epsilon = 1. /((episode / 200) + 1)

    while not done:
        #clock.tick(200)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, (255, 0, 0), env.robot, 0)
        if level == 3:
            for i in range(6):
                pygame.draw.rect(screen, (135,206,250), env.obs_rects[i], 0)
            for i in range(6,10):
                #Moving
                pygame.draw.rect(screen, (255, 215, 0), env.obs_rects[i], 0)
        if level == 4:
            for i in range(5):
                pygame.draw.rect(screen, (135,206,250), env.obs_rects[i], 0)
            for i in range(5,8):
                #Moving
                pygame.draw.rect(screen, (255, 215, 0), env.obs_rects[i], 0)
        if level == 6:
            for i in range(6):
                pygame.draw.rect(screen, (135,206,250), env.obs_rects[i], 0)
            #Moving
            pygame.draw.rect(screen, (255, 215, 0), env.obs_rects[6], 0)
            #Moving 2
            pygame.draw.rect(screen, (255,20,147), env.obs_rects[7], 0)
        if level == 9:
            for obs in env.obs_rects:
                pygame.draw.rect(screen, (135,206,250), obs, 0)
                
#        if level == 8:
#            for i in range(10):
#                pygame.draw.rect(screen, (135,206,250), env.obs_rects[i], 0)
#            for i in range(10,13):
#                #Moving
#                pygame.draw.rect(screen, (255, 215, 0), env.obs_rects[i], 0)
            
                
                
        pygame.draw.rect(screen, (0, 255, 0), env.goal, 0)
        

        if np.random.rand() < epsilon:
            action = np.random.randint(0, GameConstants.ACTION_SPACE_SIZE)
        else:

            action = np.argmax(game.main_model.predict(curr_state.reshape(-1, *curr_state.shape)))
    

        next_state, reward, done = env.step(action)
        transition = (curr_state, action, reward, next_state, done)
        replay_buffer.append(transition)
        mini_batch_size = GameConstants.MINI_BATCH_SIZE
        if episode>200:
            minibatch = random.sample(replay_buffer, mini_batch_size)
            error = game.train_dqn(minibatch)
            
            

        episode_reward += reward
        episode_step += 1
        curr_state = next_state


        pygame.display.update()

    if episode % GameConstants.STEPS_PER_TARGET_UPDATE == 0:
        game.target_model.set_weights(game.main_model.get_weights())

    list_ep_rewards.append(episode_reward)
    avg_ep_reward = np.mean(list_ep_rewards)
    print(f'episode: {episode}, reward: {episode_reward:.2f}, steps: {episode_step}, eps: {epsilon:.2f}, level: {level}', end='')
    f.write(f'episode: {episode}, reward: {episode_reward:.2f}, steps: {episode_step}, level: {level}')


    if reward == GameConstants.OBSTACLE_PENALTY:
        print(', -obstacle collision-')
        penalty += 1
        f.write(', -obstacle collision-\n')
        list_goal_reached.append(0)
    elif reward == GameConstants.GOAL_REWARD:
        print(', -goal found-')
        prize += 1
        f.write(', -goal found-\n')
        list_goal_reached.append(1)
        # main_model.save(f'epreward/{episode_reward}_steps/{steps} .model')
    else:
        print()
        f.write('\n')
        list_goal_reached.append(0)

    if (episode+1) % GameConstants.EPISODE_REPORT_COUNT == 0:
        print('\nResults up till now')
        print('obstacle collision: ', penalty)
        print('goal found: ', prize)
        print('max step: ', GameConstants.EPISODE_REPORT_COUNT - penalty - prize)
        list_average_rewards.append(np.mean(list_ep_rewards[-GameConstants.EPISODE_REPORT_COUNT:]))
        print('mean reward: ',list_average_rewards[-1])
        f.write(f'\nResults up till now\nobstacle collision: {penalty}\ngoal found: {prize}\nmax step: {episode - penalty - prize}\nmean reward: {np.mean(list_ep_rewards[-GameConstants.EPISODE_REPORT_COUNT:])}\n\n')
        end = time.time()
        penalty, prize = 0, 0
        print('Elapsed time: ',end-start)
        start = time.time()
        game.main_model.save(f'model-{list_average_rewards[-1]:.2f}.h5')
        #game.target_model.save(f'target_model-{list_average_rewards[-1]:.2f}.h5')

end_time = time.time()
print('Whole Time: ',end_time-start_time)

## PLOTS
reward_len=int(len(list_ep_rewards)/100)
y=[]
for i in range(reward_len):
    y.append(sum(list_ep_rewards[i*100:(i+1)*100])/100)
x = [i for i in range(reward_len)]
plt.plot(x,y)
plt.xlabel('training steps/100')
plt.ylabel('average reward')
plt.show()


reward_len=int(len(list_ep_rewards)/50)
y=[]
for i in range(reward_len):
    y.append(sum(list_ep_rewards[i*50:(i+1)*50])/50)
x = [i for i in range(reward_len)]
plt.plot(x,y)
plt.xlabel('training steps/50')
plt.ylabel('average reward')
plt.show()


goal_len=int(len(list_goal_reached)/100)
y=[]
for i in range(goal_len):
    y.append(sum(list_goal_reached[i*100:(i+1)*100]))
x = [i for i in range(goal_len)]
plt.plot(x,y)
plt.xlabel('training steps/100')
plt.ylabel('goals reached')
plt.show()


goal_len=int(len(list_goal_reached)/50)
y=[]
for i in range(goal_len):
    y.append(sum(list_goal_reached[i*50:(i+1)*50]))
x = [i for i in range(goal_len)]
plt.plot(x,y)
plt.xlabel('training steps/50')
plt.ylabel('goals reached')
plt.show()




# from keras.models import load_model

# load model
# model = load_model('model.h5')
## TEST
list_ep_rewards_test = []
penalty, prize = 0, 0
for episode in range(GameConstants.NUM_EPISODES_TEST):

    curr_state = env.reset(episode_num=episode, level=8, test = True)
    done = False
    episode_reward, episode_step = 0, 0
    epsilon = 1. / ((episode / 10) + 1)

    while not done:
        # clock.tick(200)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        pygame.draw.rect(screen, (255, 0, 0), env.robot, 0)
        for obs in env.obs_rects:
            pygame.draw.rect(screen, (255, 255, 255), obs, 0)
        pygame.draw.rect(screen, (0, 255, 0), env.goal, 0)

        action = np.argmax(game.main_model.predict(curr_state.reshape(-1, *curr_state.shape)))

        next_state, reward, done = env.step(action, test=True)

        episode_reward += reward
        episode_step += 1
        curr_state = next_state

        pygame.display.update()

    list_ep_rewards_test.append(episode_reward)
    avg_ep_reward_test = np.mean(list_ep_rewards_test)
    print(f'episode: {episode}, reward: {episode_reward:.2f}, steps: {episode_step}',end='')
    #f.write(f'episode: {episode}, reward: {episode_reward}, steps: {episode_step}')

    if reward == GameConstants.OBSTACLE_PENALTY:
        print(', -obstacle collision-')
        #f.write(', -obstacle collision-\n')
        penalty += 1
    elif reward == GameConstants.GOAL_REWARD:
        print(', -goal found-')
        #f.write(', -goal found-\n')
        prize += 1
        # main_model.save(f'epreward/{episode_reward}_steps/{steps} .model')
    else:
        print()
        #f.write('\n')

    if (episode + 1) % GameConstants.EPISODE_REPORT_COUNT == 0:
        print('\nResults up till now')
        print('obstacle collision: ', penalty)
        print('goal found: ', prize)
        print('max step: ', episode - penalty - prize)
        print('mean reward: ', np.mean(list_ep_rewards_test))
        #f.write(f'\nResults up till now\nobstacle collision: {penalty}\ngoal found: {prize}\nmax step: {episode - penalty - prize}\nmean reward: {np.mean(list_ep_rewards_test[-GameConstants.EPISODE_REPORT_COUNT:])}\n\n')


f.close()















