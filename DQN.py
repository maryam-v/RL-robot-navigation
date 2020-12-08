#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Lambda, Add, Conv2D, MaxPooling2D, Dropout, Flatten
from keras import backend as K
from keras.optimizers import Adam, RMSprop
from GameConstants import GameConstants
import numpy as np
import os





class DQN:
    def __init__(self):
        inputs = Input(shape=[20,20,2])
        down1 = Conv2D(filters=16, kernel_size=[2,2], strides=[2,2], padding='VALID', activation='relu')(inputs)
        down2 = Conv2D(filters=32, kernel_size=[2,2], strides=[2,2], padding='VALID', activation='relu')(down1)
        down2 = Conv2D(filters=128, kernel_size=[5, 5], strides=[1, 1], padding='VALID', activation='relu')(down2)
        down3 = Flatten()(down2)
        down3 = Dense(256, activation='relu')(down3)
        X = Dense(GameConstants.ACTION_SPACE_SIZE, activation='linear')(down3)
        self.main_model = Model(inputs=inputs, outputs=X)
        self.target_model = Model(inputs=inputs, outputs=X)
        self.main_model.compile(loss="mse", optimizer=Adam(lr=0.0001), metrics=['accuracy'])        
        self.target_model.set_weights(self.main_model.get_weights())

    def getMainModel(self):
        return self.main_model

    def getTargetModel(self):
        return self.target_model


    def train_dqn(self, minibatch):
        batch_states = np.array([x[0] for x in minibatch])
        batch_actions = np.array([x[1] for x in minibatch])
        batch_rewards = np.array([x[2] for x in minibatch])
        batch_next_states = np.array([x[3] for x in minibatch])
        batch_dones = np.array([x[4] for x in minibatch])
        
        
        
        main_output = self.main_model.predict(batch_states)
        target_q = main_output.copy()
        main_next_output = self.main_model.predict(batch_next_states)
        target_output = self.target_model.predict(batch_next_states)

        selected_best_actions = np.argmax(main_next_output, axis=1)
        target_output_for_selected_actions = target_output[np.arange(len(batch_states)), selected_best_actions]
        target_final_q_values_for_selected_actions = batch_rewards + GameConstants.GAMMA * target_output_for_selected_actions * (
                    1 - batch_dones)

        target_q[np.arange(len(batch_states)), batch_actions] = target_final_q_values_for_selected_actions

        self.main_model.fit(batch_states, target_q, batch_size=64, verbose=0)

        

